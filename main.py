import logging
import os

from flask import Flask, jsonify, send_file, session
from flask_socketio import SocketIO, emit

from api.odoo import variable_weight_products
from api.scale import Scale

ALLOW_ALL_ORIGINS = os.environ.get("ALLOW_ALL_ORIGINS", "False").lower() in [
    "true",
    "1",
]

logging.basicConfig(
    format="[%(asctime)s] - %(levelname)s: %(message)s", level=logging.INFO
)

app = Flask(__name__, static_folder="./client/dist/")
socket_io = SocketIO(app, cors_allowed_origins="*" if ALLOW_ALL_ORIGINS else "")


@app.route("/products")
def products():
    return jsonify(variable_weight_products())


@app.route("/api/ping")
def ping():
    return jsonify({"name": "balance-coop", "status": "ok"})


@app.after_request
def allow_all_origins(response):
    if ALLOW_ALL_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET"
    return response


@socket_io.on("connect")
def on_connect():
    logging.info("Connected ...")
    if session.get("clients_nb", 0) == 0:
        scale = Scale(socket_io)
        scale.start()
        session["scale"] = scale
        session["clients_nb"] = 0
    session["clients_nb"] += 1
    scale = session["scale"]
    emit(
        "scale_status",
        scale.status,
    )


@socket_io.on("disconnect")
def on_disconnect():
    logging.info("Disconnected ...")
    if session.get("clients_nb", 0) == 1 and session.get("scale", None):
        session["scale"].stop()
        session["scale"] = None
    session["clients_nb"] -= 1


@app.route("/")
def main():
    index_path = os.path.join(app.static_folder, "index.html")
    return send_file(index_path)


# Everything not declared before (not a Flask route / API endpoint)...
@app.route("/<path:path>")
def route_frontend(path):
    # ...could be a static file needed by the front end that
    # doesn't use the `static` path (like in `<script src="bundle.js">`)
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_file(file_path)
    # ...or should be handled by the SPA's "router" in front end
    else:
        index_path = os.path.join(app.static_folder, "index.html")
        return send_file(index_path)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

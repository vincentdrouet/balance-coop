# Balance COOP
This is the scale service for La Chouette COOP.

### Requirement
You will need :
- docker
- docker-compose

It could make your life better:
- Pycharm (Python IDE)
- Insomnia (test API)

### Build

```bash
docker-compose build
```

### Run
WEB docker needs some environment variables defined in file web.env.
```bash
ODOO_URL=https://odoo.fr/jsonrpc  # Odoo jsonrc URL
ODOO_LOGIN=...                    # Odoo user login
ODOO_PASSWORD=...                 # Odoo user password

SCALE_ADDR=127.0.0.1              # Scale ip
SCALE_PORT=65432                  # Scale port

ALLOW_ALL_ORIGINS=True            # For development only, CORS management
MOCK_SCALE=True                   # For development only, mock scale

STATIC_PATH=/app/client/dist/static
```
Then run
```bash
docker-compose up -d
```

API will be accessible to http://localhost:8000/api
```bash
curl http://localhost:8000/api/ping
```
It shall respond `{"name":"balance-coop","status":"ok"}`

### Development
```bash
poetry install
poetry run python main.py
```

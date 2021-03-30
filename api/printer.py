import logging
import math
import os
import socket
import time
from datetime import datetime

from escpos.printer import Network
from flask import abort

PRINTER_IP = os.getenv("PRINTER_IP")
RETRY_NB = 3


# Network close is called on __del__ and could raise OSError
def _close(self):
    """ Close TCP connection """
    if self.device is not None:
        try:
            self.device.shutdown(socket.SHUT_RDWR)
            self.device.close()
        except OSError:
            pass


Network.close = _close


def print_product_label(product, weight, cut, retry=0):
    if not PRINTER_IP:
        abort(400, description="Printer not configured")
    try:
        printer = Network(PRINTER_IP, timeout=10)
        if product and 0 <= weight < 100:
            name = product.get("name")
            bio = product.get("bio", False)
            cg = math.floor(weight * 1000)  # grams
            # <260><Product ID><Weight><CheckSum> / <3digits><4digits><5digits><1digit>
            barcode = f"{product.get('barcode')[0:7]}{cg:05d}"
            printer.textln(f"{name}{' BIO' if bio else ''} - {weight:.3f} Kg")
            printer.barcode(barcode, "EAN13", height=128, width=2)
            printer.ln()
        if cut:
            printer.image(img_source="logo.jpg")
            printer.textln("Les prix seront calculés en caisse")
            printer.textln("Seul le poid est encodé sur le code-barres")
            printer.ln()
            printer.textln(datetime.now().strftime("%m/%d/%Y - %H:%M"))
            printer.cut()
        printer.close()
    except Exception as e:
        logging.error(e)
        retry += 1
        if retry < RETRY_NB:
            time.sleep(1)
            print_product_label(product, weight, cut, retry)
        else:
            abort(400, description="Too many retries")

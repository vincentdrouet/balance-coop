import logging
import math
import os

from datetime import datetime
from escpos.printer import Network

PRINTER_IP = os.getenv("PRINTER_IP")


def print_product_label(product, weight, cut):
    if not PRINTER_IP:
        return
    try:
        with Network(PRINTER_IP, timeout=5) as printer:
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
                printer.textln(f"Les prix seront calculés en caisse")
                printer.textln(f"Seul le poid est encodé sur le code-barres")
                printer.ln()
                printer.textln(datetime.now().strftime("%m/%d/%Y - %H:%M"))
                printer.cut()
    except Exception as e:
        logging.error(e)

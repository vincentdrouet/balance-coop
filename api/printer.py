import logging
import math
import os

from datetime import datetime
from escpos.printer import Network

PRINTER_IP = os.getenv("PRINTER_IP")


def print_product_label(product, weight, cut):
    if not PRINTER_IP:
        return
    printer = None
    try:
        printer = Network(PRINTER_IP, timeout=5)
        printer.set(align="center", bold=True)
        if product and 0 <= weight < 100:
            name = product.get("name")
            bio = product.get("bio", False)
            cg = math.floor(weight * 10000)  # centigrams
            barcode = f"{product.get('barcode')[0:7]}{cg:06d}"  # 2600<Product ID><Weight> / <4digits><4digits><6digits>
            printer.textln(f"{name}{' BIO' if bio else ''} - {weight:.3f} Kg")
            printer.barcode(barcode, "EAN13", 128, 2, "", "")
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
    finally:
        if printer:
            printer.close()

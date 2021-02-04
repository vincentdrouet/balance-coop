import logging
import math
import os

from escpos.printer import Network

PRINTER_IP = os.getenv("PRINTER_IP", "192.168.1.48")


def print_product_label(product, weight, cut):
    name = product.get("name")
    cg = math.floor(weight * 10000)  # centigrams
    barcode = f"{product.get('barcode')[0:7]}{cg:06d}"  # 2600<Product ID><Weight> / <4digits><4digits><6digits>
    printer = None
    try:
        printer = Network(PRINTER_IP, timeout=5)
        printer.set(align="center", bold=True)
        printer.textln(f"{name} - {weight:.3f} Kg")
        printer.barcode(barcode, "EAN13", 128, 2, "", "")
        printer.ln()
        if cut:
            printer.image(img_source="logo.jpg")
            printer.textln(f"Les prix seront calculés en caisse")
            printer.cut()
    except Exception as e:
        logging.error(e)
    finally:
        if printer:
            printer.close()

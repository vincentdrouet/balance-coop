import logging
import math
import os
import socket
from datetime import datetime

from escpos.printer import Network

PRINTER_IP = os.getenv("PRINTER_IP")


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


class Printer:
    def __init__(self):
        self._printer = None

    @property
    def printer(self):
        if not PRINTER_IP:
            return None
        if not self._printer:
            self._printer = Network(PRINTER_IP, timeout=5)
            self._printer.set(align="center", bold=True)
        return self._printer

    def print_product_label(self, product, weight, cut):
        try:
            if not self.printer:
                return
            if product and 0 <= weight < 100:
                name = product.get("name")
                bio = product.get("bio", False)
                cg = math.floor(weight * 1000)  # grams
                # <260><Product ID><Weight><CheckSum> / <3digits><4digits><5digits><1digit>
                barcode = f"{product.get('barcode')[0:7]}{cg:05d}"
                self.printer.textln(f"{name}{' BIO' if bio else ''} - {weight:.3f} Kg")
                self.printer.barcode(barcode, "EAN13", height=128, width=2)
                self.printer.ln()
            if cut:
                self.printer.image(img_source="logo.jpg")
                self.printer.textln("Les prix seront calculés en caisse")
                self.printer.textln("Seul le poid est encodé sur le code-barres")
                self.printer.ln()
                self.printer.textln(datetime.now().strftime("%m/%d/%Y - %H:%M"))
                self.printer.cut()
        except Exception as e:
            logging.error(e)
            self._printer = None

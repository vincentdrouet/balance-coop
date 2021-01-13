import logging
import socket
import os

from threading import Thread
from time import sleep

from api.bizerba.message import Message
from api.bizerba.screen import Screen

MOCK_BIZEBA = os.environ.get("MOCK_BIZEBA", "False").lower() in ["true", "1"]


class Bizerba(Thread):
    def __init__(self, socket_io):
        super(Bizerba, self).__init__()
        self.addr = os.getenv("BIZERBA_ADDR")
        self.port = int(os.getenv("BIZERBA_PORT", 65432))
        self._socket_io = socket_io
        self._keep_running = True
        self._sock = None
        self._healthy = False
        self._weight = 0.0
        self._tare = 0.0
        self._last_status = {}

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def run(self):
        s = Screen()
        while self._keep_running:
            if MOCK_BIZEBA:
                import random

                self._healthy = True
                self._weight = random.random()
                self._tare = random.random()
                self._notify()
            else:
                try:
                    with socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM
                    ) as self._sock:
                        self._sock.connect((self.addr, self.port))
                        while self._keep_running:
                            m = Message(self._sock)
                            m.read()
                            self._healthy = True
                            if m.is_rle:
                                if m.header == 41:
                                    s.rle_shorts_to_grid(m.coord, m.data, m.data_length)
                                else:
                                    s.rle_bytes_to_grid(m.coord, m.data, m.data_length)
                            elif m.is_bin:
                                s.bin_to_grid(m.coord, m.data, m.data_length)

                            self._weight = s.weight
                            self._tare = s.tare
                            self._notify()
                            logging.info(
                                f"Weight: {self._weight:.3f} - Tare: {self._tare:.3f}"
                            )
                except Exception as e:
                    self._notify()
                    self.clear()
                    if self._healthy:
                        logging.error(e)
                        self._healthy = False
            sleep(2)

    @property
    def status(self):
        return {
            "healthy": self._healthy,
            "weight": self._weight if self._healthy else 0.0,
            "tare": self._tare if self._healthy else 0.0,
        }

    def _notify(self):
        if self._last_status != self.status:
            self._socket_io.emit(
                "scale_status",
                self.status,
            )
            self._last_status = self.status

    def clear(self):
        if self._sock:
            self._sock.close()
            self._sock = None

    def stop(self):
        self._keep_running = False
        self.clear()

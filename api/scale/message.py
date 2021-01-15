import logging
import socket

RIGHT_HEADER = 1
RIGHT_FOOTER = 23
RIGHT_TEXT_FOOTER = 3
TEXT_BLOCK = 2
PROT_RECT = [4, 6]
BIN_RECT = [34, 35, 36]
RLE_RECT = [39, 40, 41]
RLE_DFLT_RECT = [103, 104, 105]


class Message:
    def __init__(self, sock):
        self.sock = sock
        self.header = None
        self.data_length = None
        self.data = None
        self.footer = None
        self.coord = None

    def _recv(self, size):
        data = self.sock.recv(size)
        if len(data) == 0:
            raise socket.error("Socket server was closed")
        return int.from_bytes(data, "big")

    def _recv_header(self):
        h = self._recv(1)
        if h != RIGHT_HEADER:
            logging.warning(f"Wrong header: {self.header}")
            return
        self.header = self._recv(1)
        logging.debug(f"Received header: {self.header}")

    def _recv_coord(self):
        self.coord = (
            (self._recv(2), self._recv(2)),
            (self._recv(2), self._recv(2)),
        )
        logging.debug(f"Coordinate: {self.coord}")

    def _recv_data_length(self, size):
        self.data_length = self._recv(size)
        logging.debug(f"Data length: {self.data_length}")

    def _recv_data(self):
        if self.header == TEXT_BLOCK:
            self.data = self.sock.recv(self.data_length)
            if len(self.data) == 0:
                raise socket.error("Socket server was closed")
        else:
            self.data = [0] * self.data_length
            data_row = self.sock.recv(self.data_length)
            if len(data_row) == 0:
                raise socket.error("Socket server was closed")
            for i in range(self.data_length):
                self.data[i] = int(data_row[i])
        logging.debug(f"Received data: {self.data}")

    def _recv_footer(self):
        self.footer = self._recv(1)
        if (self.header == TEXT_BLOCK and self.footer != RIGHT_TEXT_FOOTER) or (
            self.header != TEXT_BLOCK and self.footer != RIGHT_FOOTER
        ):
            logging.warning(f"Wrong footer: {self.footer}")
        logging.debug(f"Received footer: {self.footer}")

    @property
    def is_rle(self):
        return self.header in RLE_RECT

    @property
    def is_bin(self):
        return self.header in BIN_RECT

    def read(self):
        self._recv_header()
        if self.header in BIN_RECT + RLE_RECT + RLE_DFLT_RECT:
            self._recv_coord()
            self._recv_data_length(2)
        elif self.header == TEXT_BLOCK:
            self._recv_data_length(1)
        elif self.header in PROT_RECT:
            return
        else:
            self._recv(2)  # offset
            self._recv_data_length(2)
        self._recv_data()
        self._recv_footer()

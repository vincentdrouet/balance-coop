from api.scale.digits import D_MINUS, DIGITS

SCREEN_SIZE = (64, 240)  # 64 lines - 240 columns
DIGIT_SIZE = (14, 8)

HUNDREDS_WEIGHT_DIGIT = (46, 0)
TENS_WEIGHT_DIGIT = (46, 9)
UNIT_WEIGHT_DIGIT = (46, 18)
TENTHS_WEIGHT_DIGIT = (46, 30)
HUNDREDTHS_WEIGHT_DIGIT = (46, 39)
THOUSANDTHS_WEIGHT_DIGIT = (46, 48)

TENS_TARE_DIGIT = (12, 191)
UNIT_TARE_DIGIT = (12, 200)
TENTHS_TARE_DIGIT = (12, 212)
HUNDREDTHS_TARE_DIGIT = (12, 221)
THOUSANDTHS_TARE_DIGIT = (12, 230)


class Screen:
    def __init__(self):
        self.grid = [
            [1 for _ in range(SCREEN_SIZE[1])] for _ in range(SCREEN_SIZE[0])
        ]  # [line_nb][column_nb]

    def _digit_value(self, digit_coord):
        for d, D in enumerate(DIGITS):
            find = True
            for line in range(DIGIT_SIZE[0]):
                for column in range(DIGIT_SIZE[1]):
                    d_line = digit_coord[0] + line
                    d_column = digit_coord[1] + column
                    if self.grid[d_line][d_column] != D[line][column]:
                        find = False
                        break
                if not find:
                    break
            if find:
                return d
        return 0

    def _digit_minus(self, digit_coord):
        find = True
        for line in range(DIGIT_SIZE[0]):
            for column in range(DIGIT_SIZE[1]):
                d_line = digit_coord[0] + line
                d_column = digit_coord[1] + column
                if self.grid[d_line][d_column] != D_MINUS[line][column]:
                    find = False
                    break
            if not find:
                break
        return find

    @property
    def weight(self):
        weight = 0.0
        weight += 10 * self._digit_value(TENS_WEIGHT_DIGIT)
        weight += self._digit_value(UNIT_WEIGHT_DIGIT)
        weight += 0.1 * self._digit_value(TENTHS_WEIGHT_DIGIT)
        weight += 0.01 * self._digit_value(HUNDREDTHS_WEIGHT_DIGIT)
        weight += 0.001 * self._digit_value(THOUSANDTHS_WEIGHT_DIGIT)
        if self._digit_minus(TENS_WEIGHT_DIGIT) or self._digit_minus(
            HUNDREDS_WEIGHT_DIGIT
        ):
            weight *= -1
        return weight

    @property
    def tare(self):
        tare = 0.0
        tare += 10 * self._digit_value(TENS_TARE_DIGIT)
        tare += self._digit_value(UNIT_TARE_DIGIT)
        tare += 0.1 * self._digit_value(TENTHS_TARE_DIGIT)
        tare += 0.01 * self._digit_value(HUNDREDTHS_TARE_DIGIT)
        tare += 0.001 * self._digit_value(THOUSANDTHS_TARE_DIGIT)
        return tare

    @staticmethod
    def _grid_coord(coord, i):
        length = coord[1][0] - coord[0][0]
        column = (coord[0][0] + i % length) * 8
        line = coord[0][1] + i // length
        return column, line

    def _set_in_grid(self, data, coord, i):
        column, line = self._grid_coord(coord, i)
        pixels = [int(x) for x in bin(data)[2:]]
        pixels = [0] * (8 - len(pixels)) + pixels
        try:
            for i, pixel in enumerate(pixels):
                self.grid[line][column + i] = pixel
        except IndexError:
            pass

    def bin_to_grid(self, coord, data, data_size):
        for i in range(data_size):
            self._set_in_grid(data[i], coord, i)

    def rle_bytes_to_grid(self, coord, data, data_size):
        dst_i = 0
        src_i = 0
        while src_i < data_size:
            ctrl_state = data[src_i] & 0x80
            num_repeats = data[src_i] & 0x7F
            if ctrl_state == 0:
                for j in range(num_repeats):
                    src_i += 1
                    self._set_in_grid(data[src_i], coord, dst_i)
                    dst_i += 1
            else:
                src_i += 1
                for j in range(num_repeats):
                    self._set_in_grid(data[src_i], coord, dst_i)
                    dst_i += 1
            src_i += 1

    def rle_shorts_to_grid(self, coord, data, data_size):
        dst_i = 0
        src_i = 0
        while src_i < data_size:
            num_repeats = data[src_i] & 0xFF
            src_i += 1
            num_repeats += (data[src_i] & 0x7F) << 8
            ctrl_state = data[src_i] & 0x80
            if ctrl_state == 0:
                for j in range(num_repeats * 2):
                    src_i += 1
                    self._set_in_grid(data[src_i], coord, dst_i)
                    dst_i += 1
            else:
                src_i += 1
                for j in range(num_repeats):
                    self._set_in_grid(data[src_i], coord, dst_i)
                    dst_i += 1
                    self._set_in_grid(data[src_i + 1], coord, dst_i)
                    dst_i += 1
                src_i += 1
            src_i += 1

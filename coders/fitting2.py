from collections import Counter
import sys


class Fitting2(object):
    DEFAULT_L = 6
    DEFAULT_DECREASE=3

    def __init__(self, L=DEFAULT_L, decrease_every=DEFAULT_DECREASE, decrease_by=1):
        self.L = L
        self.stats = Counter()
        self.decrease_every = decrease_every
        self.decrease_by = decrease_by

    def name(self):
        name = f'Fitting2 L={self.L};'
        if self.decrease_every > 0:
            name += f'; decrease {self.decrease_by} every {self.decrease_every}'
        return name

    def is_valid_move(data, written):
        for i in range(len(data)):
            if data[i] == '0' and written[i] == '1':
                return False
        return True

    def switch(self, data):
        return ['1' if i == '0' else '0' for i in data]

    def encode(self, data, written):
        def fail():
            return '1' * len(written), 0

        if len(written) < self.L + 2 or len(data) < self.L:
            return fail()

        length_to_try = self.L
        chunk1 = '1' + data[:length_to_try]
        chunk2 = ['0'] + self.switch(data[:length_to_try])

        offset = 0
        while not written[offset] == '0' or \
                (not Fitting2.is_valid_move(chunk1, written[offset + 1:]) and not Fitting2.is_valid_move(chunk2, written[offset+1:])):
            offset += 1
            if self.decrease_every > 0:
                length_to_try = max(1, self.L - self.decrease_by * (offset // self.decrease_every))
                chunk1 = chunk1[:length_to_try + 1]
                chunk2 = chunk2[:length_to_try + 1]

            if len(written) - offset < length_to_try + 2:
                return fail()

        self.stats[offset] += 1
        if Fitting2.is_valid_move(chunk1, written[offset + 1:]):
            self.stats['chunk1'] += 1
            succeeded = chunk1
        if Fitting2.is_valid_move(chunk2, written[offset + 1:]):
            self.stats['chunk2'] += 1
            succeeded = chunk2

        return '1' * (offset) + ''.join(written[offset: offset + 1]) + ''.join(succeeded), length_to_try

    def decode(self, data):
        decoded = []
        offset = 0
        flag_count = 0
        length_to_read = self.L
        while offset + length_to_read < len(data):
            if data[offset] == '0':
                read = data[offset + 2: offset + 2 + length_to_read]
                if data[offset + 1] == '1':
                    decoded += read
                else:
                    decoded += self.switch(read)
                offset += length_to_read + 2
                flag_count = 0
                length_to_read = self.L
            else:
                offset += 1
                flag_count += 1
                if self.decrease_every > 0:
                    length_to_read = max(1, self.L - self.decrease_by * (flag_count// self.decrease_every))
        return ''.join(decoded)


if __name__ == '__main__':
    enc, bits = encode([i for i in '111111'], '0111111')
    print(enc, bits)

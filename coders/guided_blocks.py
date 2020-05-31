from collections import Counter
import sys


class GuidedBlocks(object):
    DEFAULT_L = 6
    DEFAULT_TOGGLE = 3
    DEFAULT_DECREASE = 0

    def __init__(self, L=DEFAULT_L, toggle_every=DEFAULT_TOGGLE, decrease_every=DEFAULT_DECREASE, decrease_by=1, stride=1):
        self.L = L
        self.toggle_every = toggle_every
        self.decrease_every = decrease_every
        self.decrease_by = decrease_by
        self.stride = stride

    def name(self):
        name = f'Guided Blocks L={self.L}'
        if self.toggle_every  > 0:
            name += f'; toggle every {self.toggle_every}'
        if self.decrease_every > 0:
            name += f'; decrease {self.decrease_by} every {self.decrease_every}'
        if self.stride > 1:
            name += f'; stride: {self.stride}'
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

        if len(written) < self.L + 1 or len(data) < self.L:
            return fail()

        length_to_try = self.L
        chunk = self.switch(data[:length_to_try])

        offset = 0
        fail_counts = 0
        while not written[offset] == '0' or not GuidedBlocks.is_valid_move(chunk, written[offset + 1:]):
            fail_counts += 1
            offset += self.stride
            if self.decrease_every > 0:
                length_to_try = max(1, self.L - self.decrease_by * (fail_counts // self.decrease_every))
                chunk = chunk[:length_to_try]
            if len(written) - offset < length_to_try + 1:
                return fail()

            if self.toggle_every > 0 and offset % self.toggle_every == 0:
                chunk = self.switch(chunk)

        return '1'*(offset) + ''.join(written[offset: offset+1]) + ''.join(chunk), length_to_try

    def decode(self, data):
        decoded = []
        offset = 0
        flag_count = 0
        length_to_read = self.L
        while offset + length_to_read < len(data):
            if data[offset] == '0':
                read = data[offset + 1: offset + 1 + length_to_read]
                if self.toggle_every >  0 and (flag_count // self.toggle_every) % 2 == 1:
                    decoded += read
                else:
                    decoded += self.switch(read)

                offset += length_to_read + 1
                flag_count = 0
                length_to_read = self.L
            else:
                offset += self.stride
                flag_count += 1
                if self.decrease_every > 0:
                    length_to_read = max(1, self.L - self.decrease_by * (flag_count// self.decrease_every))
        return ''.join(decoded)
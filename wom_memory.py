class Memory(object):
    def __init__(self, length, writers, debug=False):
        self.data = ['0'] * length
        self.length = length
        self.write_offset = 0
        self.round = 0
        self.debug = debug
        self.bits_written_count = 0.
        self.round_just_changed = False
        self.writers = writers

    def max_rounds(self):
        return len(self.writers)

    def round_finished(self):
        if self.debug: print("Finished round #{}. Current capacity: {}.".format(self.round, self.capacity()))
        self.round += 1
        self.write_offset = 0
        self.round_just_changed = True

    @staticmethod
    def is_valid_move(written, to_write):
        for i in range(len(to_write)):
            if to_write[i] == '0' and written[i] == '1':
                return False
        return True

    def write(self, data, write_through_rounds=False):
        bits_encoded_sum = 0
        while len(data) > 0 and self.round < self.max_rounds():
            to_write, bits_encoded = self.writers[self.round].encode(data, self.data[self.write_offset:])
            if not to_write:
                if self.debug: print("Failed to encode. capacity {}".format(self.capacity()))
                break

            if self.write_offset + len(to_write) > len(self.data):
                if self.debug: print("Trying to write too much")
                break

            self.bits_written_count += bits_encoded
            data = data[bits_encoded:]
            bits_encoded_sum += bits_encoded
            if self.round > 0:
                if not self.is_valid_move(self.data[self.write_offset:], to_write):
                    raise Exception("Trying to write 0 on 1 at index {0}.".format(self.write_offset+i))
            self.data[self.write_offset: self.write_offset + len(to_write)] = to_write
            self.write_offset += len(to_write)
            self.round_just_changed = False
            if self.write_offset == len(self.data):
                self.round_finished()
                if not write_through_rounds:
                    break

        return bits_encoded_sum

    def read(self):
        if self.round_just_changed:
            self.round -= 1
        decoded = self.writers[self.round].decode(self.data)
        if self.round_just_changed:
            self.round += 1
        return decoded

    def capacity(self):
        return self.bits_written_count / len(self.data)

    def test(self, input):
        written = 0
        start = 0
        while True:
            succeeded = self.write(input[written:written+len(self.data)])
            written += succeeded
            if succeeded == 0:
                break
            input += input[written:written+succeeded]
            if self.round_just_changed:
                r = self.read()
                if r != input[start:written]:
                    raise Exception("FAILED!. \ninput=\t{}, \nread=\t{}, round={}, length={}".format(input[start:], r, self.round, len(self.data)))
                start = written
        return self.capacity()


def name(coders, padded=False):
    if coders[0].name() == 'RivestShamir':
        return 'RivestShamir'
    v = '{0:8}' if padded else '{}'
    return ' + '.join([v.format(i.name()) for i in coders])


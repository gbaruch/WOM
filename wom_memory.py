class Memory(object):
    def __init__(self, length, writers, debug=False, cell_order=1):
        self.data = ['0'] * length
        self.length = length
        self.write_offset = 0
        self.round = 0
        self.debug = debug
        self.bits_written_count = 0.
        self.round_just_changed = False
        self.writers = writers
        self.cell_order = cell_order

    def max_rounds(self):
        return len(self.writers)

    def round_finished(self):
        if self.debug: print("Finished round #{}. Current capacity: {}.".format(self.round, self.capacity()))
        self.round += 1
        self.write_offset = 0
        self.round_just_changed = True

    @staticmethod
    def is_valid_move(written, to_write, return_index=False):
        for i in range(len(to_write)):
            if int(to_write[i]) < int(written[i]):
                if return_index:
                    return i
                else:
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

            bits_encoded_sum += bits_encoded
            is_valid = self.is_valid_move(self.data[self.write_offset:], to_write)
            if not is_valid:
                raise Exception("Trying to write 0 on 1 at index {0}.".format(self.write_offset + self.is_valid_move(self.data[self.write_offset:], to_write, return_index=True)))
            data = data[bits_encoded:]
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


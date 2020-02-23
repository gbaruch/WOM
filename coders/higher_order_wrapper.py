import numpy as np

class HigherOrderWrapper(object):
    def __init__(self, inner_coder, order):
        self.inner_coder = inner_coder
        assert(order > 0)
        self.order = order

    def name(self):
        return 'HigherOrder<{}, {}>'.format(self.inner_coder.name(), self.order)


    def down(self, arr):
        return ['1' if i == str(self.order) else '0' for i in arr]

    def up(self, arr):
        return [str(self.order) if i == '1' else str(self.order - 1) for i in arr]

    def encode(self, data, written):
        bin_encoded, l = self.inner_coder.encode(data, self.down(written))
        if not bin_encoded: return bin_encoded, l
        return self.up(bin_encoded), l

    def decode(self, data):
        return self.inner_coder.decode(self.down(data))


if __name__ == '__main__':
    from coders import rivest_shamir

    enc = [rivest_shamir, rivest_shamir, HigherOrderWrapper(rivest_shamir, 2), HigherOrderWrapper(rivest_shamir,2)]

    text_num = 5
    data = []
    for i in range(6):
        data.append('0')
    for e in enc:
        text = format(text_num, '04b')
        start_enc = 0
        start_data = 0
        while start_enc < len(text):
            cur_data, l = e.encode(text[start_enc:], data[start_data:])
            start_enc += l
            data[start_data : start_data+len(cur_data)] = cur_data
            start_data += len(cur_data)

        decoded = e.decode(data)
        print('{} {}'.format(int(decoded, 2), decoded))
        text_num += 1

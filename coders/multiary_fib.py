class MultiaryFib(object):
    def __init__(self, m):
        self.m = m
        self.FIB_SEQ = [1, 1]
        for i in range(10000):
            self.FIB_SEQ.append(self.FIB_SEQ[-2] + self.m * self.FIB_SEQ[-1])

    def name(self):
        return f'Multiary-Fib (m={self.m})'

    def _encode_fib(self, input, start):
        encoded = []
        i = start
        while i >= 0:
            if (input // self.FIB_SEQ[i]) > 0:
                a = input // self.FIB_SEQ[i]
                encoded.append(str(a))
                input -= a * self.FIB_SEQ[i]
            else:
                encoded.append('0')
            i -= 1
        return list(reversed(encoded[:-1]))

    def fib_ratio(self, l):
        import math
        import numpy as np
        roots = np.roots([1, -self.m, -1])
        for i in roots:
            try:
                return int((l) / math.log(self.m + 1, i))
            except:
                pass
        raise Exception("couldn't find ratio for m = " + str(self.m))

    def encode(self, data, written):
        assert(max([int(i) for i in written]) == 0)
        possible_length = self.fib_ratio(len(written))
        if possible_length == 0:
            return written, 0
        input = int(data[:possible_length], 2)
        return self._encode_fib(input, len(written) - 1), possible_length

    def decode(self, data):
        input = sum([self.FIB_SEQ[i+1]*int(data[i]) for i in range(len(data))])
        output_len = self.fib_ratio(len(data))
        return format(input, '0'+str(output_len)+'b')


if __name__ == '__main__':
    for m in range(2,5):
        c = MultiaryFib(m)
        for i in range(50):
            bin_enc = format(i, 'b')
            fib_enc = ''.join(c._encode_fib(i, 10))
            enc, l = c.encode(bin_enc, '0'*int(len(bin_enc)*2))

            dec = c.decode(enc)
            if int(dec, 2) != i:
                print('Failed for m = {}, i = {}. dec={}({:03d}), {}, {}'.format(m, i, dec, int(dec, 2), enc[:l+1], dec))
                exit()
            print('{:03d}, {}'.format(int(dec, 2), ''.join(enc)))

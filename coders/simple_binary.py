def name():
    return 'Binary'


class Binary(object):
    def __init__(self, padding_ratio=0):
        self.padding_ratio = padding_ratio

    def name(self):
        name = f'Binary'
        if self.padding_ratio > 0:
            name += f', padding ratio {self.padding_ratio}'
        return name

    def encode(self, data, written):
        l = min(len(data), int((1 / (1 + self.padding_ratio)) * len(written) + 0.5))
        padding = '0' * (len(data) - l) if self.padding_ratio else ''
        return data[:l] + padding, l

    def decode(self, data):
        data_portion = int(len(data) / (1 + self.padding_ratio) + 0.5)
        return ''.join(data[:data_portion])


if __name__ == '__main__':
    import numpy as np
    def generate_random_input(length, one_ratio=0.5):
        import random
        return ''.join(["1" if random.random() < one_ratio else "0" for i in range(length)])


    for i in range(10):
        r = np.random.random()

        rand_100K = generate_random_input(100000)
        b = Binary(r)
        encoded, bits = b.encode(rand_100K, '0'*int(100000* (1 + r) + 0.5))
        d = b.decode(encoded)
        ld = len(d)
        if(d != rand_100K):
            print("Fail")
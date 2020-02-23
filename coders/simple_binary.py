def name():
    return 'Binary'


class Binary(object):
    def __init__(self, zero_every=0):
        self.zero_every = zero_every

    def name(self):
        name = f'Binary'
        if self.zero_every > 0:
            name += f', zero every {self.zero_every}'
        return name

    def encode(self, data, written):
        l = min(len(data), len(written))
        if self.zero_every == 0 or self.zero_every >= l:
            return data[:l], l

        return data[:self.zero_every] + '0', self.zero_every

    def decode(self, data):
        if self.zero_every == 0:
            return ''.join(data)
        else:
            return ''.join([i for idx, i in enumerate(data) if idx % (self.zero_every + 1) != self.zero_every])

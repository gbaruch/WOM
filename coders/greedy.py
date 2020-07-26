def name():
    return 'Greedy'


def encode(data, written):
    if len(written) < 2:
        return ["1"], 0

    if data[0] == '0':
        return ["0"], 1

    return ["1", "0"], 1


def decode(data):
    decoded = ''
    offset = 0
    while offset < len(data)-1:
        decoded += data[offset]
        offset += 1 + int(data[offset])
    return decoded


def theory(one_bit_ratio=None):
    return 1 / (1 + one_bit_ratio)
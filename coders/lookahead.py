counter = {'0': 0, '11': 0, '10': 0}

def name():
    return 'Lookahead'

def encode(data, written):
    d = data[0]

    if 1 >= len(written):
        return written, 0

    if d == '0' and written[0] == '0':
        counter['0'] += 1
        return ["0"], 1

    counter['1' + d] += 1
    return ['1', d], 1

def decode(data):
    decoded = ''
    offset = 0
    while offset + 1 < len(data):
        if data[offset] == '0':
            decoded += '0'
            offset += 1
        else:
            decoded += data[offset + 1]
            offset += 2

    return decoded

def name():
    return '2 to 1'

def encode(data, written):
    d = data[0]
    if d == '1':
        return ["1", "1"], 1
    else:
        return written[:2], 1

def decode(data):
    decoded = ['1' if data[i:i+2] == ["1", "1"] else '0' for i in range(0, len(data), 2)]
    return ''.join(decoded)


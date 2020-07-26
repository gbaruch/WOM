import wom_memory

def name():
    return 'RivestShamir'

encode_map = {0: {"00": ("0", "0", "0"),
                       "01": ("0", "0", "1"),
                       "10": ("0", "1", "0"),
                       "11": ("1", "0", "0")},
                   1: {"00": ("1", "1", "1"),
                       "01": ("1", "1", "0"),
                       "10": ("1", "0", "1"),
                       "11": ("0", "1", "1")}}
decode_map = dict((reversed(item) for item in encode_map[0].items()))
decode_map.update(dict((reversed(item) for item in encode_map[1].items())))


def encode(to_encode, written):
    if len(to_encode) < 2 or len(written) < 3:
        return written, 0

    data = to_encode[:2]

    if wom_memory.Memory.is_valid_move(written, encode_map[0][data]):
        return encode_map[0][data], 2
    else:
        return encode_map[1][data], 2


def decode(data):
    decoded = []
    for i in range(0, len(data)-2, 3):
        decoded += decode_map[tuple(data[i:i+3])]
    return ''.join(decoded)

def theory(one_bit_ratio):
    return 2/3
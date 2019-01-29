import wom_memory
is_valid_move = wom_memory.Memory.is_valid_move

def name():
    return '3 to 2'

mapping_2 =  {'00': ['110', '10100', '101010'], #B
              '01': ['111'], #A
              '11': ['011', '100', '101011'], #C
              '10': ['010', '1011']} #D

mapping_3 = {'000': '000'}

mapping_3_to_4 = {'00': '001'}

decode_map = mapping_2.copy()
for k,v in mapping_3.items():
    decode_map[k] = [v]

for k,v in mapping_3_to_4.items():
    for i in '01':
        if k+i in decode_map:
            decode_map[k+i].append(v+i)
        else:
            decode_map[k+i] = [v+i]

max_length = max(max((len(x) for x in d)) for d in decode_map.values())

def decode(data):
    decoded = ''
    data = ''.join(data)
    while len(data) > 0:
        found = False
        for code, prefixes in decode_map.items():
            for prefix in prefixes:
                if data.startswith(prefix):
                    decoded += code
                    data = data[len(prefix):]
                    found = True
                    break
            if found:
                break
        if not found:
            if len(data) < max_length:
                break #possibly no option to write more
            print("ERROR - Couldn't find prefix for data " + data)

    return decoded

def encode(data, written):
    if len(written) < 3:
        return False, 0

    if len(data) < 2:
        return False, 0
    pair = data[:2]
    if len(data) >= 3:
        triple = data[:3]

        if triple in mapping_3:
            encoding = mapping_3[triple]
            if is_valid_move(written, encoding):
                return encoding, 3

        if pair in mapping_3_to_4:
            encoding = mapping_3_to_4[pair]
            if len(encoding) + 1 <= len(written) and is_valid_move(written, mapping_3_to_4[pair] + data[2]):
                return encoding + data[2], 3

    for prefix in mapping_2[pair]:
        if len(prefix) <= len(written) and is_valid_move(written, prefix):
            return prefix, 2
    return False, 0

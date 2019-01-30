import wom_memory
is_valid_move = wom_memory.Memory.is_valid_move


def name():
    return '5 to 3'

mapping_3 =  {'000': ['11111'],                                                                             #A
              '001': ['11101', '01110', '10010'],                                                           #B
              '010': ['10111', '01011'],                                                                    #C
              '100': ['11100', '11011', '101010111'],                                              #D '00101'
              '101': ['11110', '101010110', '101010001', '10101010100', '101010101010'],  #E '11001', '00111',
              '011': ['01111', '10011', '10100', '101010010', '1010101011'],                                #F
              '110': ['10110', '01010', '101010100', '101010011', '101010101011'],        #G '01101', '10001',
              '111': ['11010', '101011']}                                                          #H , '01001'

mapping_4 = {'0000': '01100',
             '0001': '11000',
             '0010': '00110',
             #'0110': '00011',
             '1000': '01000',
             '0100': '10000',  # 1001
             '0101': '00010',  # 1100
             '0011': '00100',
             #'0101': '00001',
             '1010': '00000'}

mapping_4_to_6 = {'110': ['10001', '01101'],
                  '101': ['00111', '11001'],
                  '100': ['00101'],
                  '111': ['01001']}

mapping_5_to_6 = {'0110': '00001',
                  '0000': '00011'}

decode_map = mapping_3.copy()
for k,v in mapping_4.items():
    decode_map[k] = [v]

for code, prefixes in mapping_4_to_6.items():
    for i in '01':
        if code+i not in decode_map:
            decode_map[code+i] = []
        for prefix in prefixes:
            decode_map[code+i].append(prefix + i)

for k,v in mapping_5_to_6.items():
    for i in '01':
        decode_map[k+i] = [v+i]

max_length = max(max((len(x) for x in d)) for d in decode_map.values())

def decode(data):
    decoded = ''
    data = ''.join(data)
    while len(data) > 11:
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
    if len(written) < 12 or len(data) < 3:
        return False, 0

    triplet = data[:3]
    if len(data) >= 4:
        quadruple = data[:4]

        if quadruple in mapping_5_to_6 and len(data) > 4:
            encoding = mapping_5_to_6[quadruple] + data[4]
            if 6 <= len(written) and is_valid_move(written, encoding):
                return encoding, 5

        if quadruple in mapping_4 and is_valid_move(written, mapping_4[quadruple]):
            return mapping_4[quadruple], 4

        if 6 <= len(written) and triplet in mapping_4_to_6:
            for encoding in mapping_4_to_6[triplet]:
                if is_valid_move(written, encoding+data[3]):
                    return encoding + data[3], 4

    for prefix in mapping_3[triplet]:
        if len(prefix) <= len(written) and is_valid_move(written, prefix):
            return prefix, 3
    return False, 0
def name():
    return 'Fib'

FIB_SEQ = [1, 2]
for i in range(10000):
    FIB_SEQ.append(FIB_SEQ[-2] + FIB_SEQ[-1])

def _encode_fib(input, start):
    encoded = []
    i = start
    while i >= 0:
        if input >= FIB_SEQ[i]:
            encoded.append('1')
            input -= FIB_SEQ[i]
        else:
            encoded.append('0')
        i -= 1
    return list(reversed(encoded))

def fib_ratio(l):
    return int((l - 1) / 1.44)

def encode(data, written):
    possible_length = fib_ratio(len(written))
    input = int(data[:possible_length], 2)
    return _encode_fib(input, len(written) - 1), possible_length

def decode(data):
    input = sum([FIB_SEQ[i]*int(data[i]) for i in range(len(data))])
    output_len = fib_ratio(len(data))
    return format(input, '0'+str(output_len)+'b')


def name():
    return 'old lookahead'

following_data_bits = 0


def encode(data, written):
    global following_data_bits
    d = data[0]

    if following_data_bits > 0:
        following_data_bits -= 1
        return [d], 1

    if 1 >= len(written):
        following_data_bits = 0
        return "", 0

    if d == '1':
        return ["1", "1"], 1
    else:
        if written[1] == '1':
            following_data_bits = 1
            return ["0","1"], 1
        elif written[0] == '0':
            if 2 >= len(written) or written[2] == '1':
                return ["1","0"], 1
            else:
                if 3 < len(written) and written[3] == '0':
                    following_data_bits = 2
                    return ["0", "0"], 1
                else:
                    following_data_bits = 1
                    return ["0", "1"], 1
        else:
            return ["1", "0"], 1

def decode(data):
    decoded = ''
    offset = 0
    while offset < len(data)-1:
        if data[offset: offset + 2] == ["1", "1"]:
            decoded += "1"
            offset += 2
        else:
            decoded += "0"
            offset += 2
            if offset < len(data):
                if data[offset - 1] == "1" or offset + 1 >= len(data):
                    decoded += data[offset]
                    offset += 1
                elif data[offset - 2] == "0":
                    decoded += data[offset] + data[offset + 1]
                    offset += 2

    return decoded



if __name__ == "__main__":
    import numpy as np

    counter = {'01_org':[], '01_00':[],'00': [], '11': [], '10_org': [],'10_00': [], '00_org':[], 'q=0':[]}
    p_ends = []
    p_start0 = []
    caps = []
    X = [0.5]# np.linspace(0,1,101)
    for i in X:
        v = 0
        RUNS = 1000
        for _ in range(RUNS):
            OptFib = OptimalFib(1000)
            v += OptFib.test(one_ratio = i)
            for c in counter:
                counter[c].append(OptFib.counter[c])
                p_ends.append(OptFib.p_end1)
                p_start0.append(OptFib.p_start0)
            #import sys
            #sys.stdout.flush()
        caps.append(v/float(RUNS))
    print(sum(caps))
    import matplotlib.pyplot as plt

    print('p_end1={}'.format(np.mean(p_ends)))
    print('p_start0={}'.format(np.mean(p_start0)))

    for x in counter:
        print('{}: {}'.format(x, np.mean(counter[x])))

    s = sum([np.mean(counter[x])  for x in counter if x not in ('00_org', 'q=0')])
    for c in counter:
        #plt.plot(counter[c], label = c)
        print('{}: {}'. format(c, np.mean(counter[c]) / s))
    #plt.legend()
    #plt.show()
    print('00 from 00: {}'.format(np.mean(counter['00']) / np.mean(counter['00_org'])))
    print('10 from 00: {}'.format(np.mean(counter['10_00']) / np.mean(counter['00_org'])))
    print('01 from 00: {}'.format(np.mean(counter['01_00']) / np.mean(counter['00_org'])))

import math


def name():
    return 'Ternary'


encoder = {'0':['0','0'], '1':['0','1'],'2':['1','0']}
decoder = {('0', '0'): '0', ('0', '1'): '1', ('1', '0'): '2'}


def to_ternary(n):
    if n == 0:
        return '0'
    nums = ''
    while n:
        n, r = divmod(n, 3)
        nums += str(r)#Ternary.encoder[r]
    return nums[::-1]


data_length = None


def encode(data, written):
    if len(written) < 2:
        return [], 0
    global data_length
    max_number = 3 ** (len(written) / 2) - 1
    data_length = int(math.log(max_number, 2)) - 1
    in_ter = to_ternary(int(data[:data_length],2))
    padded = '0'*int((len(written)/2 - len(in_ter))) + in_ter
    encoded = []
    for t in padded:
        encoded += encoder[t]
    return encoded, data_length


def decode(data):
    global data_length
    in_ter = ''
    for i in range(0, len(data)-1, 2):
        in_ter += decoder[tuple(data[i:i+2])]
    val = int(in_ter, 3)
    return format(val, '0'+str(data_length)+'b')

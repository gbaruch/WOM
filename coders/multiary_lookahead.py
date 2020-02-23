
class MultiaryLookahead(object):
    def __init__(self, order):
        assert(order == 3)
        self.order = order

    def name(self):
        return f'{self.order}-ary lookahead'

    def encode(self, data, written):
        #print('Encode: {0}, written {1}.'.format(data,written))
        d1 = data[0]

        if 1 >= len(written):
            return written, 0

        #if int(d1) < self.order - 1 and int(written[0]) <= int(d1):
        #    return [d1], 1

        if len(data) < 2:
            print(written, 0)
            return written, 0
        d2 = data[1]

        if int(written[0]) <= int(d1+d2, 2): #str concat, not int sum
            #print('Returning ', [str(int(d1+d2, 2)), str(self.order)], 2)
            return [str(int(d1+d2, 2)), str(self.order)], 2
        #print('getting inside')
        #if impossible to use current cell, ignore it and move to the next
        encoded, count = self.encode(data, written[1:])
        #remember to write (m-1) in the  ignored cell to know to ignore it in decoding
        encoded.insert(0, written[0])
        #print('Returning ', encoded, count)
        return encoded, count

    def decode(self, data):
        #print('Decode:', data)
        decoded = ''
        offset = 0
        while offset + 1 < len(data):
            if False and int(data[offset]) < self.order - 1:
                decoded += data[offset]
                offset += 1
            elif data[offset+1] == str(self.order):
                decoded += format(int(data[offset]), '02b')
                offset += 2
            else:
                offset += 1

        return decoded

to_encode = '000000000000'
written = ['0', '0', '3', '0', '0', '0', '0', '0', '0', '0', '0']
f = MultiaryLookahead(3)
f.encode(to_encode, written)

'''Encode: 000100, written ['0', '0', '0', '0', '0', '0'].
Encode: 0100, written ['0', '0', '0', '0'].
Encode: 00, written ['0', '0'].
Decode: ['3', '0', '3', '1', '3', '0']
______________0
FAILED!. 
input=	010000, 
read=	11010, round=1, length=6'''
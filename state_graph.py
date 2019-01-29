import random
from graphviz import Digraph

valids = []
bits = 3
assert(bits%2 == 1)
dot = Digraph(comment=str(bits) + ' bits')
ids = []
shapes ={}
for i in range(2 ** bits):
    id = format(i, '0{}b'.format(bits))
    if '11' in id:
        shape = 'circle'
    elif id.count('1') == bits / 2 + 1:
        shape = 'doubleoctagon'
    else:
        shape = 'doublecircle'
        valids.append(id)
    #if id.count("1") > bits / 2 or (id.count("1") == bits / 2 and not '11' in id):
        #dot.node(id, id, shape=shape)
    shapes[id] = shape
    ids.append(id)


def _possible_moves(id, should_recurse, backward):
    source, dest = ('0', '1') if not backward else ('1', '0')
    for i in range(bits):
        if id[i] == source:
            new = id[:i] + dest + id[i + 1:]
            yield new
            if should_recurse:
                for x in _possible_moves(new, should_recurse, backward):
                    yield x


def possible_moves(id, should_recurse, backward):
    return set(_possible_moves(id, should_recurse, backward))


def is_valid_move(source, dest):
    for i in range(len(source)):
        if source[i] == '1' and dest[i] == '0':
            return False
    return True


for id in ids:
    if True:#id.count("1") > bits/2 or (id.count("1") == bits/2 and not '11' in id):
        for possible_move in possible_moves(id, False, False):
            if True:#id.count("1") > bits/2+1:
                dot.edge(id, possible_move)
            else:
                for x in possible_moves(id, False, True):
                    if not '11' in x:
                        dot.edge(id, possible_move)
                        break
first = ord('A')
needed = set(chr(first + i) for i in range(2 ** (bits / 2 + 1)))
needed = ['yellow', 'red', 'blue', 'green', 'orange', 'cyan', 'grey', 'brown', 'hotpink', 'magenta', 'pink', 'purple', 'indigo', 'crimson', 'coral', 'beige']#, 'burlywood', 'chocolate',	'coral', 'cornflowerblue', 'fuchsia', 'maroon', 'teal',  'aqua', 'aquamarine', 'beige']
needed = set(needed[:2**(bits/2 + 1)])
it = iter(needed)
special_case = ('10' * (bits / 2 + 1))[:-1]
must = {ids[-1]: it.next(),
        special_case: it.next()}

for idx, p in enumerate(possible_moves(special_case, should_recurse=True, backward=False)):
    must[p] = it.next()

#must = {'1110011': 'green', '1110010': 'pink', '1110110': 'red', '1110111': 'indigo', '0011101': 'red', '1011101': 'hotpink', '1011100': 'magenta', '0111010': 'pink', '1111100': 'crimson', '1111101': 'coral', '1011011': 'cyan', '1011010': 'brown', '1010111': 'purple', '1010110': 'orange', '1010010': 'yellow', '1010011': 'crimson', '0111110': 'hotpink', '0111111': 'cyan', '1000101': 'crimson', '1101011': 'red', '1101010': 'crimson', '1111001': 'red', '1101110': 'indigo', '1101111': 'orange', '1001101': 'cyan', '0101110': 'yellow', '1100101': 'blue', '0011111': 'orange', '0010101': 'magenta', '1110001': 'orange', '1010100': 'cyan', '1010101': 'brown', '1011110': 'blue', '1011111': 'beige', '1111111': 'grey', '1011001': 'pink', '1110101': 'yellow', '1110100': 'pink', '1010001': 'blue', '0111101': 'pink', '1000111': 'green', '1111010': 'coral', '1111011': 'magenta', '0101010': 'blue', '0101011': 'brown', '1101101': 'red', '0110101': 'green', '0101111': 'beige', '1001111': 'pink', '1001110': 'hotpink', '1001010': 'purple', '1001011': 'yellow', '1100111': 'magenta', '0111011': 'purple', '0010111': 'blue', '0110111': 'crimson', '1111110': 'green'}
succeeded = False
counter = 0
while not succeeded:
    current = must.copy()
    succeeded = True
    random.shuffle(valids)
    for idx, id in enumerate(valids):
        if id.count('1') == int(bits / 2):
            #print("Checking ID {}".format(id))
            possibilities = possible_moves(id, True, backward=False)
            possibilities.add(id)
            existing = set(current[x] for x in possibilities if current.has_key(x))
            for x in possibilities:
                if not current.has_key(x) and len(needed.difference(existing)) > 0:
                    current[x] = random.sample(needed.difference(existing), 1)[0]
                    existing.add(current[x])

            if len(needed.difference(existing)) > 0:
                print(
                "failed at iter {}-{} on id {}. difference: {}".format(counter, idx, id, needed.difference(existing)))
                succeeded = False
                '''if len(needed.difference(existing)) <= 2: #idx > 30 and
                    succeeded=True
                    from collections import defaultdict
                    d = defaultdict(int)
                    for x in possible_moves(id, True, False):
                        d[current[x]] += 1
                        if d[current[x]] > 1:
                            print current[x]

                    print current'''
                break
    counter += 1

print("Succeeded")
#current[special_case+'0'] = current.pop(special_case)

for id in ids:
    if True:#id.count("1") > bits / 2 or (id.count("1") == bits / 2 and not '11' in id):
        for x in [1]:#possible_moves(id, False, True):
            if True:#not '11' in x or id.count("1") > bits/2+1:
                style = 'filled' if id not in ['001', git '00001','00011','10001', '01101', '00111', '11001', '00101', '01001'] else 'filled, diagonals'
                dot.node(id, id, shape=shapes[id], fillcolor=current[id] if current.has_key(id) else 'white', style=style)
                break

dot.render('graphs/{}.gv'.format(bits), view=True)



from coders import fib, greedy, map_2to1, map_3to2, map_5to3, ternary, lookahead, rivest_shamir, lookahead0


def all_combinations(include_first_rounders=False):
    coders_list = list()
    for first in [fib, greedy]:
        for second in [map_3to2, map_2to1, map_5to3, lookahead]: #lookahead0
            coders_list.append([first, second])
    coders_list.append([rivest_shamir, rivest_shamir])
    coders_list.append([ternary, map_2to1])
    if include_first_rounders:
        coders_list.append([greedy])
        coders_list.append([fib])
    return coders_list


def name(combination, padded=False):
    if combination[0].name() == 'RivestShamir':
        return 'RivestShamir'
    v = '{0:8}' if padded else '{}'
    return ' + '.join([v.format(i.name()) for i in combination])

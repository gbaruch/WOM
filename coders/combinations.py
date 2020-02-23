from coders import fib, greedy, map_2to1, map_3to2, map_5to3, ternary, lookahead, rivest_shamir, lookahead0, multiary_fib
from coders.fitting import Fitting
from coders.fitting2 import Fitting2
from coders.simple_binary import Binary

from coders.higher_order_wrapper import HigherOrderWrapper
from coders.multiary_lookahead import MultiaryLookahead


def fitting_tryouts():
    #return [[Binary(), Fitting(1,2)], [Binary(), Fitting(1)]]

    coders_list = list()

    for dec in [0, 1, 3]:
        for second in [Fitting2(i, dec) for i in range(3,8)]:
                coders_list.append([Binary(), second])

    for L in range(5,7):
        for mode in [2,3]:
            for dec in [3]:
                coders_list.append([Binary(), Fitting(L, mode, dec)])

    for L in range(3,-4):
        for mode in [2]:
            coders_list.append([Binary(), Fitting(L, mode, 0)])

    # l = len(coders_list)
    # for j in range(10):
    #     coders_list.append(coders_list[-1] + [Fitting(6, 3, 3)])

    coders_list.append([greedy, lookahead])
    coders_list.append([rivest_shamir, rivest_shamir])

    return coders_list


def all_combinations(include_first_rounders=True, include_non_switched_fittings=False):
    coders_list = list()
    switched = [True, False] if include_non_switched_fittings else [True]
    coders_list.append([Binary(), Fitting(3, 0)])
    coders_list.append([Binary(), Fitting(6, 3, 3)])
    for first in [fib, greedy]:
        for second in [lookahead]: #, map_3to2, map_2to1, map_5to3#lookahead0
            coders_list.append([first, second])
    coders_list.append([rivest_shamir, rivest_shamir])
    #coders_list.append([ternary, map_2to1])
    if include_first_rounders:
        coders_list.append([greedy])
        coders_list.append([fib])

    return coders_list


Names = {}

def name(combination, padded=False):
    if tuple(combination) in Names:
        return Names[tuple(combination)]

    if combination[0].name() == 'RivestShamir':
        return 'RivestShamir'
    v = '{0:8}' if padded else '{}'
    return ' + '.join([v.format(i.name()) for i in combination])


def repeater(for_each_round, cell_order):
    l = for_each_round[:]
    for i in range(2, cell_order + 1):
        for coder in for_each_round:
            l.append(HigherOrderWrapper(coder, i))

    Names[tuple(l)] = 'Repeater <{}, m={}>'.format(name(for_each_round, False), cell_order)
    return l


def multiary_combinations(cell_order):
    leveled_fib = repeater([fib, lookahead], cell_order)
    leveled_greedy = repeater([greedy, lookahead], cell_order)
    rs_list = repeater([rivest_shamir, rivest_shamir], cell_order)
    mfc = [multiary_fib.MultiaryFib(cell_order), HigherOrderWrapper(lookahead, cell_order)]

    if cell_order == 3:
        return [[multiary_fib.MultiaryFib(cell_order), MultiaryLookahead(cell_order)], mfc, rs_list]

    return [leveled_fib, mfc, rs_list, leveled_greedy]

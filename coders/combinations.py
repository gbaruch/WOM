from coders import fib, greedy, map_2to1, map_3to2, map_5to3, ternary, lookahead, rivest_shamir, multiary_fib
from coders.guided_blocks import GuidedBlocks
from coders.simple_binary import Binary
from coders.two_sided_guided_blocks import TwoSidedGuidedBlocks
from coders.higher_order_wrapper import HigherOrderWrapper
from coders.multiary_lookahead import MultiaryLookahead


def for_3d():
    return [[greedy, lookahead]]


def theory_tryouts():
    coders_list = list()
    for L in [3, 6]:
        for complement in [False, True]:
            for with_padding in [True, False]:
                padding = 1 / L if with_padding else 0
                coders_list.append([Binary(padding), TwoSidedGuidedBlocks(L, L, with_complement=complement)])
    return coders_list


def with_guided_blocks():
    coders_list = list()
    for first in [greedy, fib]:
        for second in [lookahead]:
            coders_list.append([first, second])

    coders_list.append([rivest_shamir, rivest_shamir])
    coders_list.append([rivest_shamir, rivest_shamir, GuidedBlocks(3, 3)])

    for L in [2, 5, 8, 11]:
        coders_list.append([Binary(), GuidedBlocks(L, 1, 0)])
    return coders_list


def on_real_data():
    coders_list = list()

    coders_list.append([greedy, lookahead])

    coders_list.append([rivest_shamir, rivest_shamir])

    coders_list.append([Binary(), GuidedBlocks(3, 1)])
    coders_list.append([Binary(), GuidedBlocks(6, 3, 0)])
    coders_list.append([Binary(), GuidedBlocks(6, 3, 3)])

    return coders_list


def three_writes():
    coders_list = list()

    coders_list.append([greedy, lookahead])
    coders_list.append([rivest_shamir, rivest_shamir])
    coders_list.append([Binary(), GuidedBlocks(6, 3, 3)])
    coders_list.append([Binary(), GuidedBlocks(3, 1)])

    l2 = list()
    for i in coders_list:
        l2.append(i + [GuidedBlocks(3, 1)])

    return l2


def all_combinations(include_first_rounders=True, include_non_switched_fittings=False, add_fitting_to_all=False):

    coders_list = list()
    for first in [greedy, fib]:
        for second in [lookahead, map_3to2, map_5to3]:
            coders_list.append([first, second])

    coders_list.append([rivest_shamir, rivest_shamir])

    coders_list.append([Binary(), GuidedBlocks(3)])
    coders_list.append([Binary(), GuidedBlocks(6, 3, 3)])

    coders_list.append([ternary, map_2to1])
    if include_first_rounders:
        coders_list.append([greedy])
        coders_list.append([fib])

    if add_fitting_to_all:
        l = len(coders_list)
        for i in coders_list[:l]:
            i.append(GuidedBlocks(3, 3))

    return coders_list


Names = {}

def name(combination, padded=False):
    if tuple(combination) in Names:
        return Names[tuple(combination)]
    v = '{0:8}' if padded else '{}'

    if combination[0].name() == 'RivestShamir':
        name = 'RivestShamir'
        if len(combination) > 2:
            return ' + '.join([name] + [v.format(i.name()) for i in combination[2:]])
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

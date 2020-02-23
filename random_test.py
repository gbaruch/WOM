import itertools
import matplotlib
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

import wom_memory
from coders import combinations

MAX_PROB = 0.5

def file_name(coders, resolution, mem_size, cell_order):
    return 'logs/{}_res{}_mem{}{}.npy'.format(coders if type(coders) == str else combinations.name(coders), resolution, mem_size, '' if cell_order == 1 else f'_order{cell_order}')


def plot_3d(combos, resolution, mem_size, order, coolwarm_cmap=False):
    from matplotlib import cm
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib as mpl


    fig = plt.figure()
    ax = fig.gca(projection='3d')

    fake_lines = []
    labels = []
    visibility = []
    surfaces = []
    rax = plt.axes([0.05, 0.3, 0.2, 0.5])
    for combo in combos:
        vals = np.load(file_name(combo, resolution, mem_size, order))
        X = np.linspace(0.01, MAX_PROB, resolution)
        X, Y = np.meshgrid(X, X)
        surf = ax.plot_surface(X, Y, np.mean(vals, axis=2), visible=False, cmap=cm.coolwarm if coolwarm_cmap else None)
        surfaces.append(surf)
        labels.append(combinations.name(combo))
        visibility.append(False)
    check = CheckButtons(rax, labels, visibility)
    if coolwarm_cmap:
        fig.colorbar(surf)
    ax.legend(fake_lines, labels)
    ax.set_xlabel('1-bit Probability - First  Round')
    ax.set_ylabel('1-bit Probability - Second Round')
    ax.set_zlabel('Compression Ratio')

    def func(label):
        index = labels.index(label)
        surfaces[index].set_visible(not surfaces[index].get_visible())
        plt.draw()

    check.on_clicked(func)

    plt.show()


def fitting_theory(prob_one, L):
    prob_for_a_fit = (1 - prob_one) * ((1 - prob_one * prob_one) ** L)

    probs = [(1 - prob_for_a_fit) **  i  * prob_for_a_fit for i in range(300)]
    expected_count_of_failures = sum([probs[i] * i for i in range(300)])
    return 1 + L / (1 + L + expected_count_of_failures)


def interactive_legend(ax=None):
    from InteractiveLegend import InteractiveLegend
    if ax is None:
        ax = plt.gca()
    if ax.legend_ is None:
        ax.legend()

    return InteractiveLegend(ax.get_legend())


def plot_results(coders_list, resolution, length, cell_order):

    X = np.linspace(0.01, MAX_PROB, resolution)

    markers = itertools.cycle(('o', 's', '*', '+', '>', 'p', 'x', '<', '4', 'D'))
    fig, ax = plt.subplots()
    for coders in coders_list:
        try:
            vals = np.load(file_name(coders, resolution, length, cell_order))
        except OSError:
            print("Warning: couldn't find " + file_name(coders, resolution))
            continue
        name = combinations.name(coders)
        means = [np.mean(vals[i, i, :]) for i in range(len(X))]
        label = name.replace(' + ', r'$\rightarrow$') + ' [{:.2f}]'.format(sum(means) / 2 / len(means))
        ax.plot(X, means, label=label, marker=next(markers))
        # m = next(markers)
        # for idx, x in enumerate(X):
        #     ax.scatter([x] * count, vals[idx, idx], label=label if idx == 0 else None, marker=m)
    sota = 1.493
    ax.plot([0, MAX_PROB],[sota, sota], linestyle='--', color='grey', label='SOTA [{:.2f}]'.format(sota / 2))#sota

    handles, labels = plt.gca().get_legend_handles_labels()
    # sort both labels and handles by labels
    '''labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0], reverse=True))
    labels, handles = list(labels), list(handles)
    if len(labels) > 1:
        labels[0], labels[1] = labels[1], labels[0]
        handles[0], handles[1] = handles[1], handles[0]'''
    fig.subplots_adjust(bottom=0.55)
    ax.legend(handles, labels, frameon=False, loc='lower center', bbox_to_anchor=(0.5, -1.55),
              ncol=2, borderaxespad=0)
    plt.xlabel('1-bit probability', )
    plt.ylabel('compression ratio')
    leg = interactive_legend()

    plt.show()

def generate_random_input(length, one_ratio=0.5):
    import random
    return ''.join(["1" if random.random() < one_ratio else "0" for i in range(length)])


def test_round(mem, input):
    written = 0
    while True:
        succeeded = mem.write(input[written:written+len(mem.data)])
        written += succeeded
        if not succeeded or mem.round_just_changed:
            r = mem.read()
            if len(r) != written:
                raise Exception(
                    "FAILED! len(read) != written. \ninput=\t{}, \nread=\t{}, round={}, length={}".format(input,
                                                                                r, mem.round, len(mem.data)))
            if r != input[:written]:
                print("FAILED!. \ninput=\t{}, \nread=\t{}, round={}, length={}".format(input, r,
                                                                                     mem.round, len(mem.data)))
                for k in range(written):
                    if r[k] != input[k]:
                        raise Exception("FAILED!. \ninput=\t{}, \nread=\t{}, round={}, length={}".format(input[:k+1], r[:k+1], mem.round, len(mem.data)))
            return mem.capacity()


def generate_random_results(coders_list, resolution=50, count=100, length=1002, cell_order=1):
    if resolution > 1:
        X = np.linspace(0.01, MAX_PROB, resolution)
    else:
        X = [0.5]
    print('{0:60}: ratio_at_0.5'.format('Name'))
    print('_'*75)
    print_stats = False
    for coders in coders_list:
        print('{0:60}: '.format(combinations.name(coders, True)), end='')
        vals = np.empty((len(X), len(X), count))
        X_ind = [0,0]
        for X_ind[0] in range(len(X)):
            for X_ind[1] in [X_ind[0]]:#range(len(X)):
                for c in range(count):
                    wom = wom_memory.Memory(length, coders, cell_order=cell_order)
                    for k in range(len(coders)):
                        val = test_round(wom, generate_random_input(length, one_ratio=X[X_ind[k % 2]]))
                    vals[X_ind[0], X_ind[1], c] = val

                    if print_stats and hasattr(coders[-1], 'print_stats'):
                        print(f'printing stats for  {coders[-1].name()} at prob {X[X_ind[1]]}')
                        coders[-1].print_stats()
                        coders[-1].reset_stats()
        np.save(file_name(coders, resolution, length, cell_order), vals)
        print("{0:.3f}".format(np.mean(vals[-1, -1, :])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--resolution", default=3, type=int)
    parser.add_argument("-c", "--iteration_count", default=10, type=int)
    parser.add_argument("-m", "--memory_size", default=4002, type=int)
    parser.add_argument("-2", "--plot_2d", default=True, type=bool)
    parser.add_argument("-3", "--plot_3d", default=False, type=bool)
    parser.add_argument("-g", "--generate_results", default=True, type=bool)
    parser.add_argument("-o", "--cell_order", default=1, type=int)

    args = parser.parse_args()
    print(f"Evaluating WOM methods on random data with {args.resolution} data points between 0 and 0.5,"
          f" averaged over {args.iteration_count} iterations each. Memory Size = {args.memory_size}.")

    if args.cell_order == 1:
        coders_list = combinations.all_combinations(include_first_rounders=False)
    else:
        coders_list = combinations.multiary_combinations(args.cell_order)

    if args.resolution == 1:
        print('Not plotting when resolution is 1')
        args.plot_2d = args.plot_3d = False
    #coders_list = combinations.fitting_tryouts()

    if args.generate_results:
        generate_random_results(coders_list, args.resolution, args.iteration_count, args.memory_size, args.cell_order)

    if args.plot_3d:
        plot_3d(coders_list, args.resolution, args.memory_size, args.cell_order)
        plt.show()

    if args.plot_2d:
        plot_results(coders_list, args.resolution, args.memory_size, args.cell_order)


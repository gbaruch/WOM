import itertools
import matplotlib
import argparse
import numpy as np
import matplotlib.pyplot as plt

import wom_memory
from coders import fib, greedy, map_2to1, map_3to2, map_5to3, ternary, lookahead, rivest_shamir, lookahead0


def file_name(coders, resolution):
    return 'logs/{}_res{}.csv'.format(wom_memory.name(coders), resolution)


def plot_results(coders_list, resolution):
    X = np.linspace(0.01, 0.5, resolution)

    markers = itertools.cycle((',',',','o', 's','*', '+', '>', 'p', 'x', '<', '4','D'))

    matplotlib.rcParams.update({'font.size': 14})

    for coders in coders_list:
        try:
            vals = np.loadtxt(file_name(coders, resolution))
        except OSError:
            print("Warning: couldn't find " + file_name(coders, resolution))
            continue
        name = wom_memory.name(coders)
        plt.plot(X, np.mean(vals, axis=1), label=name.replace(' to ', r'$\rightarrow$'), marker = next(markers))

    handles, labels = plt.gca().get_legend_handles_labels()
    # sort both labels and handles by labels
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0], reverse=True))
    labels, handles = list(labels), list(handles)
    if len(labels) > 1:
        labels[0], labels[1] = labels[1], labels[0]
        handles[0], handles[1] = handles[1], handles[0]
    plt.legend(handles, labels, frameon=False, ncol=3)

    plt.xlabel('1-bit probability', )
    plt.ylabel('compression ratio')


def generate_random_input(length, one_ratio = 0.5):
    import random
    return ''.join(["1" if random.random() < one_ratio else "0" for i in range(length)])


def generate_random_results(coders_list, resolution=50, count=100, length=1002):
    X = np.linspace(0.01, 0.5, resolution)
    print('{0:25}: ratio_at_0.5'.format('Name'))
    print('_'*35)
    for coders in coders_list:
        print('{0:25}: '.format(wom_memory.name(coders, True)), end='')
        vals = []
        for i in X:
            vals.append([])
            for _ in range(count):
                wom = wom_memory.Memory(length, coders)
                vals[-1].append(wom.test(generate_random_input(length*3, one_ratio = i)))
        np.savetxt(file_name(coders, resolution), vals)
        print("{0:.3f}".format(np.mean(vals, axis=1)[-1]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--resolution", default=50, type=int)
    parser.add_argument("-c", "--iteration_count", default=100, type=int)
    parser.add_argument("-m", "--memory_size", default=1002, type=int)
    parser.add_argument("-p", "--plot_results", default=True, type=bool)
    parser.add_argument("-g", "--generate_results", default=True, type=bool)

    args = parser.parse_args()
    print(f"Evaluating WOM methods on random data with {args.resolution} data points between 0 and 0.5,"
          f" averaged over {args.iteration_count} iterations each. Memory Size = {args.memory_size}.")
    coders_list = list()
    for first in [greedy, fib]:
        for second in [map_2to1, map_3to2, map_5to3, lookahead]: #lookahead0
            coders_list.append([first, second])
    coders_list.append([rivest_shamir, rivest_shamir])
    coders_list.append([ternary, map_2to1])
    coders_list.append([greedy])
    coders_list.append([fib])

    if args.generate_results:
        generate_random_results(coders_list, args.resolution, args.iteration_count, args.memory_size)

    if args.plot_results:
        plot_results(coders_list, args.resolution)
    plt.title('WOM evaluated on random data')
    plt.show()

import itertools
import matplotlib
import argparse
import numpy as np
import matplotlib.pyplot as plt

import wom_memory
from coders import combinations

def file_name(coders, resolution):
    return 'logs/{}_res{}.npy'.format(coders if type(coders) == str else combinations.name(coders), resolution)


def plot_3d(combos, resolution, coolwarm_cmap=False):
    from matplotlib import cm
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib as mpl
    from matplotlib.widgets import CheckButtons

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    fake_lines = []
    labels = []
    visibility = []
    surfaces = []
    rax = plt.axes([0.05, 0.3, 0.2, 0.5])
    for combo in combos:
        vals = np.load(file_name(combo, resolution))
        X = np.linspace(0.01, 0.5, resolution)
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


def plot_results(coders_list, resolution):

    X = np.linspace(0.01, 0.5, resolution)

    markers = itertools.cycle((',',',','o', 's','*', '+', '>', 'p', 'x', '<', '4','D'))
    matplotlib.rcParams.update({'font.size': 14})

    for coders in coders_list:
        try:
            vals = np.load(file_name(coders, resolution))
        except OSError:
            print("Warning: couldn't find " + file_name(coders, resolution))
            continue
        name = combinations.name(coders)
        means = [np.mean(vals[i, i, :]) for i in range(len(X))]
        plt.plot(X, means, label=name.replace(' to ', r'$\rightarrow$'), marker = next(markers))

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
                for k in range(written):
                    if r[k] != input[k]:
                        raise Exception("FAILED!. \ninput=\t{}, \nread=\t{}, round={}, length={}".format(input[:k+1], r[:k+1], mem.round, len(mem.data)))
            return mem.capacity()


def generate_random_results(coders_list, resolution=50, count=100, length=1002):
    X = np.linspace(0.01, 0.5, resolution)
    print('{0:25}: ratio_at_0.5'.format('Name'))
    print('_'*35)
    for coders in coders_list:
        print('{0:25}: '.format(combinations.name(coders, True)), end='')
        vals = np.empty((len(X), len(X), count))
        X_ind = [0,0]
        for X_ind[0] in range(len(X)):
            for X_ind[1] in range(len(X)):
                for c in range(count):
                    wom = wom_memory.Memory(length, coders)
                    for k in range(len(coders)):
                        val = test_round(wom, generate_random_input(length, one_ratio=X[X_ind[k]]))
                    vals[X_ind[0], X_ind[1], c] = val
        np.save(file_name(coders, resolution), vals)
        print("{0:.3f}".format(np.mean(vals[-1, -1, :])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--resolution", default=50, type=int)
    parser.add_argument("-c", "--iteration_count", default=10, type=int)
    parser.add_argument("-m", "--memory_size", default=1002, type=int)
    parser.add_argument("-2", "--plot_2d", default=False, type=bool)
    parser.add_argument("-3", "--plot_3d", default=True, type=bool)
    parser.add_argument("-g", "--generate_results", default=True, type=bool)

    args = parser.parse_args()
    print(f"Evaluating WOM methods on random data with {args.resolution} data points between 0 and 0.5,"
          f" averaged over {args.iteration_count} iterations each. Memory Size = {args.memory_size}.")

    coders_list = combinations.all_combinations()

    if args.generate_results:
        generate_random_results(coders_list, args.resolution, args.iteration_count, args.memory_size)


    if args.plot_3d:
        plot_3d(coders_list, args.resolution)
    if args.plot_2d:
        plt.figure()
        plt.title('WOM evaluated on random data')
        plot_results(coders_list, args.resolution)

    plt.show()

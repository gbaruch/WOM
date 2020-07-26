import itertools
import matplotlib
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

import wom_memory
from coders import combinations

MAX_PROB = 0.5

SUFFIX = ''
def file_name(coders, resolution, mem_size, cell_order):
    fn = 'logs/{}_res{}_mem{}{}.npy'.format(coders if type(coders) == str else combinations.name(coders), resolution, mem_size, '' if cell_order == 1 else f'_order{cell_order}')
    if SUFFIX != '':
        fn += SUFFIX + '.npy'
    return fn


def plot_3d(combos, resolution, mem_size, order, coolwarm_cmap=True):
    from matplotlib import cm
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib as mpl

    use_plotly = True
    if not use_plotly:
        fig = plt.figure()
        ax = fig.gca(projection='3d')

    SOTA = 1.509

    fake_lines = []
    labels = []
    visibility = []
    surfaces = []

    #rax = plt.axes([0.05, 0.3, 0.2, 0.5])
    plotly_objects = []
    for combo in combos:
        vals = np.load(file_name(combo, resolution, mem_size, order))
        X = np.linspace(0.01, MAX_PROB, resolution)
        X, Y = np.meshgrid(X, X)
        means = np.mean(vals, axis=2)

        if use_plotly:
            import plotly.graph_objects as go
            plotly_objects.append(go.Surface(z=means, x=X, y=Y, colorscale='RdBu_r'))
            plotly_objects.append(go.Scatter3d(z=[means[x, x] + 0.005 for x in range(len(X[0]))], x=X[0], y=X[0],
                                               line=
                                                  go.Line(
                                                      color="#000000",
                                                      width=5.
                                                  ),
                                               marker=dict(size=0, color='rgba(0,0,0,0)')))

            if True:
                z = np.zeros_like(X)
                z[:] = SOTA
                plotly_objects.append(
                    go.Surface(z=z, x=X, y=Y, opacity=0.5, colorscale=[[0, 'rgb(0,255,0)'], [1, 'rgb(0,255,0)']]))

            N = 50
            fig = go.Figure(data=plotly_objects)

            fig.update_layout(scene=dict(
                xaxis=dict(
                    title="1-bit Probability - First Round",
                    gridcolor="grey",
                    showbackground=True,
                    zerolinecolor="black",
                    zerolinewidth=10,
                    ticktext=[f'  {i}  ' for i in [0, 0.1, 0.2, 0.3, 0.4, 0.5]],
                    tickvals= [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
                    ticks='outside',
                    range=[0.00, 0.5]),
                yaxis=dict(
                    title="1-bit Probability - Second Round",
                    gridcolor="grey",
                    showbackground=True,
                    zerolinecolor="black",
                    zerolinewidth=10,
                    ticktext=[f'  {i}  ' for i in [0, 0.1, 0.2, 0.3, 0.4, 0.5]],
                    tickvals= [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
                    ticks='outside',
                    range=[0.00, 0.5]),
                zaxis=dict(
                    title="Compression Ratio",
                    gridcolor="grey",
                    showbackground=True,
                    zerolinecolor="white",
                    zerolinewidth=10,
                    ticks='outside',
                ), ),
                scene_aspectmode='cube',
                font=dict(size=17),
                margin=dict(r=10, l=10, b=10, t=10)

            )

            '''fig.update_layout(scene=dict(
                xaxis_title="1-bit Probability - First Round",
                yaxis_title="1-bit Probability - Second Round",
                zaxis_title="Compression Ratio"),
                scene_aspectmode='cube',
                xaxis_gridcolor='rgb(0,255,0)',
                yaxis_gridcolor='rgb(0,255,0)',
                xaxis=dict(
                    gridcolor="white",
                    zerolinecolor="white", ),
                yaxis=dict(
                    gridcolor="white",
                    zerolinecolor="white"),
                

            )'''
            fig.show()
        else:


            SOTA_z = np.empty_like(means)
            SOTA_z[:] = SOTA



            #surf.set_sort_zpos(1)
            SOTA_z_parital = SOTA_z.copy()
            SOTA_z_parital[means < SOTA] = np.nan
            SOTA_z[~(means < SOTA)] = np.nan
            surf3 = ax.plot_wireframe(X, Y, SOTA_z_parital, rstride=10, cstride=10, zorder=20, color='green')
            # surf2.set_sort_zpos(0)

            ax.plot(X[0], X[0], [means[x, x] for x in range(len(X[0]))], lw=5, c='black', zorder=10)

            surf = ax.plot_surface(X, Y, means, visible=True, cmap=cm.coolwarm if coolwarm_cmap else None, linewidth=0, zorder=2)

            import matplotlib.cm as cm
            m = cm.ScalarMappable(cmap=cm.coolwarm)
            m.set_array(means)
            plt.colorbar(m)

            surf2 = ax.plot_wireframe(X, Y, SOTA_z, rstride=10, cstride=10, zorder=20, color='green')


            surfaces.append(surf)
            labels.append(combinations.name(combo))
            visibility.append(True)




    if not use_plotly:

        ax.set_xlabel('1-bit Probability - First Round')
        ax.set_ylabel('1-bit Probability - Second Round')
        ax.set_zlabel('Compression Ratio')
        plt.xlim(0.02, 0.5)
        plt.ylim(0.02, 0.5)

        if False:
            if coolwarm_cmap:
                fig.colorbar(surf)

            check = CheckButtons(rax, labels, visibility)

            ax.legend(fake_lines, labels)

            def func(label):
                index = labels.index(label)
                surfaces[index].set_visible(not surfaces[index].get_visible())
                plt.draw()

            check.on_clicked(func)

        plt.show()


def interactive_legend(ax=None):
    from InteractiveLegend import InteractiveLegend
    if ax is None:
        ax = plt.gca()
    if ax.legend_ is None:
        ax.legend()

    return InteractiveLegend(ax.get_legend())


def theory_plots(Ls, ax, X):
    from coders.two_sided_guided_blocks import TwoSidedGuidedBlocks

    def w_wo(b):
        return 'w' if b else 'wo'

    for L in Ls:
        for settings in range(2):
            with_padding = settings // 2
            with_complement = settings % 2
            vals = [
                TwoSidedGuidedBlocks.theory(L, one_prob=x, with_padding=with_padding, with_complement=with_complement)
                for x in X]
            ax.plot(X, vals,
                    label='GuidedBlocks Theory - L={0}, stride=L+1, {1} complement'.format(L, w_wo(with_complement)))


def plot_results(coders_list, resolution, length, cell_order, writes=2, plot_theory=False, plot_SOTA=True):

    X = np.linspace(0.01, MAX_PROB, resolution)
    amount_to_skip = int((0.05-0.01) / MAX_PROB * resolution)
    markers = itertools.cycle(('o', 's', '*', '+', '>', 'p', 'x', '<', '4', 'D'))
    fig, ax = plt.subplots()

    if plot_theory:
        Ls = set([c[1].L for c in coders_list if len(c) > 1 and hasattr(c[1], 'L')])
        theory_plots(Ls, ax, X)

    for coders in coders_list:
        try:
            vals = np.load(file_name(coders, resolution, length, cell_order))
        except OSError:
            print("Warning: couldn't find " + file_name(coders, resolution, length, cell_order))
            continue
        name = combinations.name(coders)
        means = [np.mean(vals[i, i, :]) for i in range(len(X))]
        label = name.replace(' + ', r'$\rightarrow$')
        ax.plot(X[amount_to_skip:], means[amount_to_skip:], label=label, marker=next(markers))

        try:
            ax.plot(X[amount_to_skip:], [sum(c.theory(q) for c in coders) for q in X[amount_to_skip:]], label=label + " - Theory")
        except:
            pass
    if plot_SOTA:
        SOTA = {2: 1.509}#, 3: 1.61}
        ax.plot([0, MAX_PROB], [SOTA[writes], SOTA[writes]], linestyle='--', label='SOTA for {} writes [{:.2f}]'.format(writes, SOTA[writes]))

    handles, labels = plt.gca().get_legend_handles_labels()
    # sort both labels and handles by labels
    '''labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0], reverse=True))
    labels, handles = list(labels), list(handles)
    if len(labels) > 1:
        labels[0], labels[1] = labels[1], labels[0]
        handles[0], handles[1] = handles[1], handles[0]'''
    fig.subplots_adjust(bottom=0.25)
    ax.legend(handles, labels, frameon=False, loc='lower center', bbox_to_anchor=(0.5, -0.25),
              ncol=2, borderaxespad=0)
    plt.xlabel('1-bit probability', )
    plt.ylabel('compression ratio')
    #leg = interactive_legend()

    import tikzplotlib

    tikzplotlib.save("gb_random_test_plot.tex")

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
                    f"FAILED! len(read) ({len(r)}) != written ({written}). " + "\ninput=\t{}, \nread=\t{}, round={}, length={}".format(input,
                                                                                r, mem.round, len(mem.data)))
            if r != input[:written]:
                print("FAILED!. \ninput=\t{}, \nread=\t{}, round={}, length={}".format(input, r,
                                                                                     mem.round, len(mem.data)))
                for k in range(written):
                    if r[k] != input[k]:
                        raise Exception("FAILED!. \ninput=\t{}, \nread=\t{}, round={}, length={}".format(input[:k+1], r[:k+1], mem.round, len(mem.data)))
            return mem.capacity()


def generate_random_results(coders_list, resolution=50, count=100, length=1002, cell_order=1, three_d=False):
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
            if three_d:
                r = range(len(X))
            else:
                r = [X_ind[0]]
            for X_ind[1] in r:
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
    parser.add_argument("-r", "--resolution", default=11, type=int)
    parser.add_argument("-c", "--iteration_count", default=100, type=int)
    parser.add_argument("-m", "--memory_size", default=1000, type=int)
    parser.add_argument("-t", "--theory", default=False, type=bool)
    parser.add_argument("-2", "--plot_2d", default=True, type=bool)
    parser.add_argument("-3", "--plot_3d", default=False, type=bool)
    parser.add_argument("-g", "--generate_results", default=True, type=bool)
    parser.add_argument("-o", "--cell_order", default=1, type=int)
    parser.add_argument("-w", "--writes", default=2, type=int)

    args = parser.parse_args()
    print(f"Evaluating WOM methods on random data with {args.resolution} data points between 0 and 0.5,"
          f" averaged over {args.iteration_count} iterations each. Memory Size = {args.memory_size}.")

    if args.plot_3d:
        coders_list = combinations.for_3d()
    elif args.theory:
        coders_list = combinations.theory_tryouts()
    else:
        if args.cell_order == 1:
            if args.writes == 2:
                coders_list = combinations.all_combinations(include_first_rounders=False)#with_guided_blocks
            if args.writes == 3:
                coders_list = combinations.three_writes()
        else:
            coders_list = combinations.multiary_combinations(args.cell_order)

    if args.resolution == 1:
        print('Not plotting when resolution is 1')
        args.plot_2d = args.plot_3d = False

    if args.writes == 3:
        SUFFIX = '_3w'

    if args.generate_results:
        generate_random_results(coders_list, args.resolution, args.iteration_count, args.memory_size, args.cell_order, three_d=args.plot_3d)

    if args.plot_3d:
        plot_3d(coders_list, args.resolution, args.memory_size, args.cell_order)
        plt.show()

    if args.plot_2d:
        plot_results(coders_list, args.resolution, args.memory_size, args.cell_order, writes=args.writes, plot_theory=args.theory)


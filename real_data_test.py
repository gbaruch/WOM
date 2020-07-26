import argparse

import wom_memory
from coders import combinations

def test_type(bits_data, wom_type, blocks_count, cells_count):
    woms = []
    succeeded = 0
    while len(woms) < blocks_count:
        woms.append(wom_memory.Memory(cells_count, wom_type))
        succeeded += woms[-1].write(bits_data[succeeded:])
    read = ''
    for w in woms:
        read += w.read()
    #read_text = ''.join((chr(int(read[i:i + 8], 2)) for i in range(0, len(read), 8)))

    if read != bits_data[:len(read)]:
        for i in range(0, len(read), 10):
            if read[i: i + 10] != bits_data[i:i + 10]:
                print("failed")
                print(read[i:i + 10])
                print(bits_data[i:i + 10])
    assert (read == bits_data[:len(read)])

    for wom in woms:
        succeeded += wom.write(bits_data[succeeded:])

    return succeeded


def test_file(data_folder, filename, wom_types, cells_count = 600, blocks_count = 100):
    print('{0:30}, '.format(filename), end='')
    with open(data_folder + filename, 'rb') as f:
        data = f.read(cells_count*blocks_count*3)

    bits_data = ''.join([format(i,'08b') for i in data])

    one_bit_prob = float(bits_data.count('1')) / len(bits_data)
    print('{0:20.3f}, '.format(one_bit_prob), end='')
    print('{0:15}'.format(cells_count*blocks_count), end='')

    results = {}
    for coders in wom_types:
        name = combinations.name(coders).replace('+', '+\n')
        res = test_type(bits_data, coders, blocks_count, cells_count)
        results[name] = res / cells_count / blocks_count
        print(', {0:18.3f}'.format(results[name]), end='')

    print('')
    return results, one_bit_prob


if __name__ == '__main__':
    import os
    import sys
    from time import gmtime, strftime

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data_directory", default='data/', type=str)
    parser.add_argument("-m", "--memory_size", default=600, type=int)
    parser.add_argument("-c", "--iteration_count", default=100, type=int)
    parser.add_argument("-s", "--save", action='store_true')
    parser.add_argument("-p", "--plot", action='store_true')

    args = parser.parse_args()
    print(
        f'\nEvaluating WOM methods on data from the folder "{args.data_directory}". {args.iteration_count} blocks of {args.memory_size} bits each.')

    coders_list = combinations.on_real_data()

    if args.save:
        out_filename = strftime("results_%Y-%m-%d %H-%M.csv", gmtime())

        old_stdout = sys.stdout
        print('Saving results to ', out_filename)
        sys.stdout = open(os.path.join(args.data_directory, out_filename), 'wt')

    print('{0:30}, {1:11}, {2:10}'. format('Directory', 'Memory Size' ,'Iterations'))
    print('{0:30}, {1:11}, {2:10}'.format(args.data_directory, args.memory_size, args.iteration_count))
    print('\nResults:')
    print('{0:30}, {1:20}, {2:15}'.format('File Name', '1-bit probability', 'Overall Cells'),end='')
    for coders in coders_list:
        print(', {0:<18}'.format(combinations.name(coders)), end='')
    print('')

    files = os.listdir(args.data_directory)
    results = {}
    one_bit_prob = {}
    for file_name in files:
        if file_name.startswith('results') or os.path.isdir(os.path.join(args.data_directory, file_name)) or file_name[0] == '.':
            continue
        results[file_name], one_bit_prob[file_name] = test_file(args.data_directory, file_name, coders_list, args.memory_size, args.iteration_count)

    if args.save:
        sys.stdout.close()
        sys.stdout = old_stdout
        print('Done')

    if args.plot or True:
        import pandas as pd
        import matplotlib.pyplot as plt
        df = pd.DataFrame(results).T
        df.index = ['{0:}\n({1:.1f}% 1-bits)'.format(key.split('.')[0], one_bit_prob[key] * 100) for key in df.index]

        df.plot(kind='barh')

        if False:
            plt.figure()

            for key in results:
                plt.plot(list(results[key].keys()), list(results[key].values()), label='{0:30} ({1:.2f}% 1-bits)'.format(key, one_bit_prob[key] * 100))

            plt.legend()

        import tikzplotlib

        tikzplotlib.save("plots/real_data_plot.tex")

        plt.show()
    exit()

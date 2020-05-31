from collections import Counter, defaultdict
import sys

import matplotlib.pyplot as plt


class TwoSidedGuidedBlocks(object):
    def __init__(self, L=3, stride=None, toggle_every=0, with_complement=True):
        self.L = L
        self.stride = stride if stride is not None else L
        self.toggle_every = toggle_every
        self.with_complement = with_complement

    def name(self):
        name = f'2-Sided GB L={self.L}'
        name += f'; stride={self.stride}'
        if self.with_complement:
            name += '; w. complement'
        if self.toggle_every > 0:
            name += f'; toggle every={self.toggle_every}'
        return name

    def is_valid_move(data, written):
        for i in range(len(data)):
            if data[i] == '0' and written[i] == '1':
                return False
        return True

    def switch(self, data):
        return ['1' if i == '0' else '0' for i in data]

    def inner_encode(self, data, written):
        def fail():
            return '1' * len(written), 0, 0#int(len(written) / (1 + self.L))

        if len(written) < self.L + 1 or len(data) < self.L:
            return fail()

        length_to_try = self.L
        if self.with_complement:
            chunk = ''.join(self.switch(data[:length_to_try]))
        else:
            chunk = ''.join(data[:length_to_try])

        offset = 0
        while not written[-1 - offset] == '0' or not TwoSidedGuidedBlocks.is_valid_move(chunk, written[offset*self.stride:]):
            offset += 1

            if self.toggle_every > 0 and offset % self.toggle_every == 0:
                chunk = ''.join(self.switch(chunk))

            if len(written) < length_to_try + offset * (self.stride + 1) + 1:
                return fail()

        return '1' * self.stride * offset + chunk, length_to_try, offset

    def encode(self, data, written):
        data_offset= 0
        flags, data_to_write = '', ''
        while True:
            current_data_to_write, data_bits, current_offsets = self.inner_encode(data[data_offset:], written[len(data_to_write):len(written)-len(flags)])
            data_to_write += current_data_to_write
            if data_bits == 0:
                break

            block = data[data_offset:data_offset + data_bits]

            data_offset += data_bits
            flags = '0' + '1' * current_offsets + flags
        #print("Flags ", len(flags) + current_offsets)
        return data_to_write + flags, data_offset


    def decode(self, data):
        decoded = []
        data_offset, flag_count, current_flag_count = 0, 0 ,0
        length_to_read = self.L

        while data_offset + flag_count + length_to_read + 1 <= len(data):
            if data[-1-flag_count] == '0':
                read = data[data_offset: data_offset + length_to_read]
                if self.toggle_every > 0 and (current_flag_count // self.toggle_every) % 2 == 1:
                    decoded += read
                else:
                    if self.with_complement:
                        decoded += self.switch(read)
                    else:
                        decoded += read

                data_offset += length_to_read
                current_flag_count = 0
            else:
                data_offset += self.stride
                current_flag_count += 1
            flag_count += 1

        return ''.join(decoded)

    @staticmethod
    def theory(L, with_padding=True, with_complement=True, one_prob=0.5):
        def n_choose_k(n, k):
            import math
            f = math.factorial
            return f(n) / f(k) / f(n - k)

        expected_offset_count = 0
        for ones_count in range(L + 1):
            zeros_count = L - ones_count
            possibilities = n_choose_k(L, ones_count)
            prob_for_appearance_for_each = one_prob ** ones_count * (1 - one_prob) ** zeros_count

            if with_complement:
                prob_for_success = (1 - one_prob) ** ones_count
            else:
                prob_for_success = (1 - one_prob) ** zeros_count

            if not with_padding:
                prob_for_success *= 1 - one_prob

            expected_offset = 1 / prob_for_success

            expected_offset_count += possibilities * prob_for_appearance_for_each * expected_offset

        if with_padding:
            first_round = 1 / (1 + 1/L)
        else:
            first_round = 1
        second_round = L / (expected_offset_count) / (L + 1)

        return first_round + second_round


    @staticmethod
    def theory_wrong(L, with_padding=True, with_complement=False, one_prob=0.5):
        second_round_one_prob = (1 - one_prob) if with_complement else one_prob
        prob_for_a_fit = (1 - (one_prob * second_round_one_prob)) ** L
        if not with_padding:
            prob_for_a_fit *= 1 - one_prob

        probs = [(1 - prob_for_a_fit) ** i * prob_for_a_fit for i in range(200)]
        expected_count_of_failures = sum([probs[i] * (i + 1) for i in range(200)])

        if with_padding:
            first_round = 1 / (1 + 1/L)
        else:
            first_round = 1

        second_round = L / expected_count_of_failures / (L + 1)

        return first_round + second_round


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import wom_memory
    from coders.simple_binary import Binary
    import numpy as np


    def generate_random_input(length, one_ratio=0.5):
        import random
        return ''.join(["1" if random.random() < one_ratio else "0" for i in range(length)])

    memory_size = 50000

    import itertools
    markers = itertools.cycle(('o', 's', '*', '+', '>', 'p', 'x', '<', '4'))

    def w_wo(val):
        return 'w' if val else 'wo'

    with_toggle = False
    main_L = 7
    one_probs = np.linspace(0.01, 0.5, 6)
    for with_complement in [True, False]:
        for with_padding in [False, True]:

            label = ' L = {2}, {0} Padding, {1}. complement'.format(w_wo(with_padding), w_wo(with_complement), main_L)
            res = [TwoSidedGuidedBlocks.theory(main_L, one_prob=one_prob, with_padding=with_padding, with_complement=with_complement) for one_prob in one_probs]
            plt.plot(one_probs, res, label='Theory' + label, marker=next(markers))

            res = [TwoSidedGuidedBlocks.theory_wrong(main_L, one_prob=one_prob, with_padding=with_padding,
                                               with_complement=with_complement) for one_prob in one_probs]
            plt.plot(one_probs, res, label='Wrong Theory' + label, marker=next(markers))

            label = ' L = {2}, {0}. Padding, {1}. complement'.format(w_wo(with_padding), w_wo(with_complement), main_L)

            caps = []
            for one_prob in one_probs:
                wom = wom_memory.Memory(memory_size, [Binary(1 / main_L if with_padding else 0),
                                                      TwoSidedGuidedBlocks(main_L, main_L, toggle_every=0, with_complement=with_complement)])
                res = wom.write(generate_random_input(memory_size, one_prob))
                res = wom.write(generate_random_input(memory_size, one_prob))
                caps.append(wom.capacity())

            plt.plot(one_probs, caps, label='Real' + label, marker=next(markers))
    plt.legend()
    plt.xlabel('One probability')
    plt.ylabel('Capacity')
    plt.show()
    exit()
    second_Ls = list(range(1, 10)) + list(range(10, 20, 2))
    plt.figure()
    for with_toggle in [False]:
        for with_padding in False, True:
            Ls = range(1, 20)
            label = ' {0}. Padding, {1}. toggle'.format('w' if with_padding else 'wo', 'w' if with_toggle > 0 else 'wo')

            if not with_toggle:
                res_w = [TwoSidedGuidedBlocks.theory(l, with_padding=with_padding, with_complement=with_toggle) for l in Ls]
                plt.plot(Ls, res_w, label='Theory' + label)

            capacities = []

            second_Ls = list(range(1,10)) + list(range(10, 20, 2))
            for main_L in second_Ls:
                wom = wom_memory.Memory(memory_size, [Binary(1/main_L if with_padding else 0), TwoSidedGuidedBlocks(main_L, main_L,  with_toggle)])
                res = wom.write(generate_random_input(memory_size))
                print(main_L, 'First round:', res, 'Capacity:', wom.capacity())
                res = wom.write(generate_random_input(memory_size))
                print(main_L, 'Second round:', res, 'Capacity:', wom.capacity())
                capacities.append(wom.capacity())

            plt.plot(second_Ls, capacities, label='Real' + label)

    plt.legend()
    plt.show()
    exit()

    main_L = 7
    fitting = TwoSidedGuidedBlocks(main_L, 3, 1)
    l = 20
    written = generate_random_input(l) + '0'*int(l / main_L)
    to_write = generate_random_input(l)
    encoded, bits = fitting.encode(to_write, written)
    if not TwoSidedGuidedBlocks.is_valid_move(encoded, written):
        print(written)
        print(to_write)
        print("Assertion!")
    r = fitting.decode(encoded)
    if r == to_write[:bits]:
        print(f"Succeeded writing {bits} bits in {len(encoded)}")
    else:
        print("Failed")
        print(written, to_write)

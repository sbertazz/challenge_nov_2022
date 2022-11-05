import itertools
import time


def run_coin_machine(amount_str):
    available_coins = [1, 2, 5, 10, 20, 50, 100, 200]
    start = time.time()
    try:
        pound, pence = amount_str.replace('£', '').split('-')
        amount = int(pound) * 100 + int(pence)
    except:
        raise Exception('Input should be in this format: £x-xx, eg £2-31, £0-54')

    # the maximum length of the combination is a combination of [1, 1, ..., 1]
    # amount = 80
    max_sol_length = amount

    # we start from the longest combination, and then remove 1 dimension at the time. for each combination, we should prune the
    # once that we know are not possible. we can maybe sort and
    curr_length = 0  # max_sol_length
    possible_combos = []
    while curr_length <= max_sol_length:
        if available_coins[-1] + curr_length - 1 > amount:
            print(f'removing {available_coins[-1]}')
            available_coins.pop()
            print(available_coins)
        if curr_length % 2 == 0:
            curr_length += 1
        else:
            print(curr_length)
            all_combos = itertools.combinations_with_replacement(available_coins, r=curr_length)
            active_combo = next(all_combos)
            while active_combo[0] <= amount:
                #             print(active_combo)

                if sum(active_combo) == amount:
                    possible_combos.append(active_combo)
                try:
                    active_combo = next(all_combos)
                except:
                    break
            curr_length += 1

    print(time.time() - start)

    print(f'Number of combos: {len(possible_combos)}')



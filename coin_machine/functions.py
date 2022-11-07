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

    # we start from the shortes combinations, and then add 1 dimension at the time. for each combination, we should prune the
    # ones that we know are not possible.
    curr_length = 0  # max_sol_length
    possible_combos = []
    while curr_length <= max_sol_length:
        if available_coins[-1] + curr_length - 1 > amount:
            # print(f'removing {available_coins[-1]}')
            available_coins.pop()
            # print(available_coins)
        if curr_length % 2 == 0:
            curr_length += 1
        else:
            # print(curr_length)
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

    print(f'time: {time.time() - start}')

    print(f'Number of combos: {len(possible_combos)}')

    return possible_combos


def _get_coins_combinations(amount, denominations, combos, i=0, parent=None):
    if parent is None:
        parent = []
    if amount == 0:
        if len(parent) % 2 ==1:
            combos.append(parent)
#             print(combos)
        return 1
    elif amount < 0:
        return None
    else:
        s = 0
        for i in range(i, len(denominations)):
            coin = denominations[i]
#             print(f'coin {coin}, amount {amount}')
            if amount - coin < 0:
                break
#                 c = _get_num_of_changes(amount - coin, denominations, i+1, new_parent)
            else:
                new_parent = parent.copy() + [coin]
#                 print(f'new parent: {new_parent}')
                c = _get_coins_combinations(amount - coin, denominations, combos, i, new_parent)

            if c:
                s += c
        return s


def run_coin_machine_v2(amount_str):
    start = time.time()
    available_coins = [1, 2, 5, 10, 20, 50, 100, 200]
    try:
        pound, pence = amount_str.replace('£', '').split('-')
        pence = 0 if pence == '' else pence  # support amounts like £2-
        amount = int(pound) * 100 + int(pence)
    except:
        raise Exception('Input should be in this format: £x-xx, eg £2-31, £0-54')
    combos = []
    res = _get_coins_combinations(amount, available_coins, combos)
    print(f'time: {time.time() - start}')
    print(f'number of combinations: {len(combos)}')
    return combos

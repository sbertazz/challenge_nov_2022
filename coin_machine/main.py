from coin_machine.functions import run_coin_machine, run_coin_machine_v2

amount_str = '£10-'

# combinations_1 = run_coin_machine(amount_str)

combinations_2 = run_coin_machine_v2(amount_str)

# Compute follow inputs: £0-50, £2-, £10-, (£100- for extra marks)
# £0-50: 225
# £2-:  36840
# £10-:
# £100-:

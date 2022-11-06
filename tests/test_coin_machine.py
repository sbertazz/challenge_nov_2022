from coin_machine.functions import run_coin_machine_v2


def test_coin_machine():
    assert len(run_coin_machine_v2('£2-')) == 36840  # 8.31
    assert len(run_coin_machine_v2('£0-31')) == 58  # 8.31


def test_coin_machine_output_type():
    assert type(run_coin_machine_v2('£0-5')) == list

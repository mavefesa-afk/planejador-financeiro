from core.calculations import real_rate, withdrawal_rate

def test_real_rate():
    value = real_rate(0.10, 0.04)
    assert round(value, 6) == round((1.10 / 1.04) - 1, 6)

def test_withdrawal_rate():
    assert withdrawal_rate(2000, 350000) == (24000 / 350000)

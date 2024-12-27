import pytest

from src.bank_account import BankAccount


@pytest.mark.parametrize("ammount, expected", [(0, 1000), (-500, 1000), (500, 1500)])
def test_deposit_vr_ammounts(ammount, expected):
    account = BankAccount(balance=1000, log_file='test_account_1.txt')
    new_balance = account.deposit(ammount)
    assert new_balance == expected
    

def test_sum():
    assert 1 + 2 == 3


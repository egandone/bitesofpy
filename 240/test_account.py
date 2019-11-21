import pytest
from account import Account

# write your pytest functions below, they need to start with test_

def test_ordering():
    account1 = Account('owner1')
    assert str(account1) == 'Account of owner1 with starting amount: 0'
    assert repr(account1) == 'Account(\'owner1\', 0)'
    account2 = Account('owner2', 0)
    assert str(account2) == 'Account of owner2 with starting amount: 0'
    assert repr(account2) == 'Account(\'owner2\', 0)'
    assert account1 == account2

    account1.add_transaction(10)
    assert account1 != account2
    assert account1 > account2
    assert account2 < account1

    account1.add_transaction(-10)
    assert account1 == account2
    assert not account1 < account2
    assert not account1 > account2

    assert account1.balance == 0
    assert account2.balance == 0
    assert account1[0] == 10
    assert account1[1] == -10

def test_account_add():
    account1 = Account('owner1',20)
    account1.add_transaction(10)
    account1.add_transaction(5)
    account1.add_transaction(1)
    account1.add_transaction(1)
    account1.add_transaction(1)
    assert str(account1) == 'Account of owner1 with starting amount: 20'
    assert repr(account1) == 'Account(\'owner1\', 20)'
    assert account1.balance == 38

    account2 = Account('owner2', 100)
    assert str(account2) == 'Account of owner2 with starting amount: 100'
    assert repr(account2) == 'Account(\'owner2\', 100)'
    account2.add_transaction(20)
    assert account2.balance == 120
    
    account1 += account2
    assert account1.owner == 'owner1&owner2'
    assert account1.balance == 158

def test_errors():
    account = Account('owner', 50)
    with pytest.raises(ValueError) as ve:
        account.add_transaction(4.5)
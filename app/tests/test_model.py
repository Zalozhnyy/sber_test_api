import pytest

from app.model import Deposit
from pydantic import ValidationError

@pytest.fixture
def base_data() -> dict:
    return {
        'date': "10.11.2021",
        'periods': 3,
        'amount': 40000,
        'rate': 5
    }


def test_correct_deposit(base_data):
    Deposit(**base_data)


def test_raise_date_in_future(base_data):
    with pytest.raises(ValidationError) as e:
        base_data['date'] = "10.11.2028"
        Deposit(**base_data)


def test_raise_amount(base_data):
    with pytest.raises(ValidationError) as e:
        base_data['amount'] = 9999999
        Deposit(**base_data)


def test_raise_periods(base_data):
    with pytest.raises(ValidationError) as e:
        base_data['periods'] = 0
        Deposit(**base_data)


def test_raise_rate(base_data):
    with pytest.raises(ValidationError) as e:
        base_data['rate'] = 9999
        Deposit(**base_data)


@pytest.mark.xfail
def test_empty_deposit():
    Deposit()

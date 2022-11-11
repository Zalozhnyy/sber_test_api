import pytest
from datetime import date

from app.model import Deposit
from app.business_logic.deposit_calculator import DepositCalculator, DepositCalculatorResult
from .test_model import base_data


def test_first_month():
    _date = date(2000, 1, 31)
    incremented_date = DepositCalculator._increment_month(_date, is_first=True)
    assert _date == incremented_date


def test_month_increment():
    _date = date(2000, 1, 1)

    incremented_date = DepositCalculator._increment_month(_date)

    assert date(_date.year, 2, 29) == incremented_date

    incremented_date = DepositCalculator._increment_month(date(_date.year, 2, 29))

    assert date(_date.year, 3, 31) == incremented_date


def test_year_increment():
    _date = date(2000, 12, 1)

    incremented_date = DepositCalculator._increment_month(_date)

    assert date(_date.year + 1, 1, 31) == incremented_date


def test_deposit_benefit():
    value = DepositCalculator._calc_deposit_percents(100, 12)

    assert value == 101.


def test_deposit_calculation(base_data):
    d = Deposit(**base_data)

    res = DepositCalculator(d).calculate()

    assert res.values[0] == d.amount + (d.amount * d.rate / 100 / 12)
    assert res.dates[0] == date(d.date.year, 11, 30)


def test_get_results_as_json():
    dates = [date(2000, i, i) for i in range(1, 13)]
    values = [i for i in range(1, 13)]

    r = DepositCalculatorResult(dates, values).as_json()

    for key, ori_dat, ori_val in zip(r, dates, values):
        assert key == ori_dat.strftime("%d.%m.%Y")
        assert r[key] == ori_val

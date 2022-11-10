import json

from pydantic import BaseModel, validator
from datetime import date, datetime, timedelta

import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent
with open(BASE_DIR / 'constraints.json', 'r') as f:
    constraints = json.load(f)


class DateInFuture(Exception): pass


class PeriodsValidationError(Exception): pass


class AmountValidationError(Exception): pass


class RateValidationError(Exception): pass


class Deposit(BaseModel):
    date: date
    periods: int
    amount: int
    rate: float

    @validator('date', pre=True)
    def validate_date(cls, v: str):
        """transform DD.MM.YYYY to YYYY-MM.DD"""
        _date = v.split('.')[::-1]
        return '-'.join(_date)

    @validator('date')
    def validate_date_lte_now(cls, v: date):
        if date.today() < v:
            raise DateInFuture()
        return v

    @validator('periods')
    def validate_periods(cls, v):
        l, r = constraints['periods']['min'], constraints['periods']['max']
        if v < l or v > r:
            raise PeriodsValidationError(f'periods not in [{l}, {r}]')
        return v

    @validator('amount')
    def validate_amounts(cls, v):
        l, r = constraints['amount']['min'], constraints['amount']['max']
        if v < l or v > r:
            raise AmountValidationError(f'amount not in [{l}, {r}]')
        return v

    @validator('rate')
    def validate_rate(cls, v):
        l, r = constraints['rate']['min'], constraints['rate']['max']
        if v < l or v > r:
            raise RateValidationError(f'rate not in [{l}, {r}]')
        return v


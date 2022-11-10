from app.model import Deposit
from dataclasses import dataclass

from datetime import date, timedelta
from calendar import monthrange
import json


@dataclass
class DepositCalculatorResult:
    dates: list[date]
    values: list[float]

    def as_json(self) -> str:
        res = dict()
        for _date, val in zip(self.dates, self.values):
            res[_date.strftime("%d.%m.%Y")] = round(val, 2)

        return json.dumps(res, indent=4)

    def as_json_impl2(self) -> str:  # на мой взгляд более правильный Response json
        return json.dumps(
            {
                "dates": [_date.strftime("%d.%m.%Y") for _date in self.dates],
                "values": [round(val, 2) for val in self.values],
            }
            , indent=4
        )


class DepositCalculator:

    def __init__(self, dep: Deposit):
        self._deposit: Deposit = dep

    def _increment_month(self, _date: date) -> date:

        if _date.month == 12:  # december
            return date(_date.year + 1, 1, 31)

        last_day = monthrange(_date.year, _date.month + 1)[1]
        return date(_date.year, _date.month + 1, last_day)

    def _calc_deposit_percents(self, val: float) -> float:
        return val + (val * self._deposit.rate / 12 / 100)

    def calculate(self) -> DepositCalculatorResult:
        values = [self._deposit.amount]
        dates = [self._deposit.date]

        for i in range(self._deposit.periods):
            dates.append(self._increment_month(dates[-1]))
            values.append(self._calc_deposit_percents(values[-1]))

        return DepositCalculatorResult(dates[1:], values[1:])


d = Deposit(**{
    'date': "1.1.2021",
    'periods': 24,
    'amount': 100,
    'rate': 1
})


from app.model import Deposit
from dataclasses import dataclass

from datetime import date
from calendar import monthrange
import json


@dataclass
class DepositCalculatorResult:
    dates: list[date]
    values: list[float]

    def as_json(self) -> dict:
        res = dict()
        for _date, val in zip(self.dates, self.values):
            res[_date.strftime("%d.%m.%Y")] = round(val, 2)

        return res

    def as_json_impl2(self) -> str:
        # на мой взгляд более правильный Response json
        return json.dumps(
            {
                "dates": [_date.strftime("%d.%m.%Y") for _date in self.dates],
                "values": [round(val, 2) for val in self.values],
            },
            indent=4,
        )


class DepositCalculator:
    def __init__(self, dep: Deposit):
        self._deposit: Deposit = dep

    @staticmethod
    def _increment_month(_date: date, is_first: bool = False) -> date:

        if is_first:
            return date(_date.year, _date.month, monthrange(_date.year, _date.month)[1])

        if _date.month == 12:  # december
            return date(_date.year + 1, 1, 31)

        last_day = monthrange(_date.year, _date.month + 1)[1]
        return date(_date.year, _date.month + 1, last_day)

    @staticmethod
    def _calc_deposit_percents(val: float, rate: float) -> float:
        return val + (val * rate / 12 / 100)

    def calculate(self) -> DepositCalculatorResult:
        values = [self._deposit.amount]
        dates = [self._deposit.date]

        for i in range(self._deposit.periods):
            dates.append(self._increment_month(dates[-1], is_first=len(dates) == 1))
            values.append(self._calc_deposit_percents(values[-1], self._deposit.rate))

        return DepositCalculatorResult(dates[1:], values[1:])

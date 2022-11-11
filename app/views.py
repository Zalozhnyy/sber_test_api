from aiohttp import web
from aiohttp.web import json_response
from pydantic import ValidationError

from app.model import Deposit
from app.business_logic.deposit_calculator import DepositCalculator


async def calc_deposit(request: web.Request) -> web.Response:
    if request.content_type != "application/json":
        return json_response({'error': f'content_type {request.content_type} not supported'}, status=400)

    body = await request.json()

    try:
        deposit = Deposit(**body)
        return json_response(
            DepositCalculator(deposit).calculate().as_json()
        )

    except ValidationError as e:
        return json_response({"error": e.errors()}, status=400)
    except Exception as e:
        return json_response({"error": e.__str__()}, status=400)

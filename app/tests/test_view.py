import json

from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer
import pytest

from app.views import calc_deposit
from main import setup_routes


async def hello(request):
    return web.Response(text='Hello, world')


@pytest.fixture
def cli(event_loop, aiohttp_client):
    app = web.Application()
    setup_routes(app)
    return event_loop.run_until_complete(aiohttp_client(app))


@pytest.fixture
def example_body():
    return {
        'date': "31.01.2021",
        'periods': 7,
        'amount': 10000,
        'rate': 6
    }


@pytest.mark.asyncio
async def test_get_results(cli, example_body):
    resp = await cli.get('/', json=example_body)

    data = await resp.json()
    assert resp.status == 200

    expected = {
        "31.01.2021": 10050,
        "28.02.2021": 10100.25,
        "31.03.2021": 10150.75,
        "30.04.2021": 10201.51,
        "31.05.2021": 10252.51,
        "30.06.2021": 10303.78,
        "31.07.2021": 10355.29,
    }
    for k1, k2 in zip(data, expected):
        assert k1 == k2
        assert data[k1] == expected[k2]


@pytest.mark.asyncio
async def test_two_month_with_31(cli, example_body):
    example_body['periods'] = 2

    resp = await cli.get('/', json=example_body)

    data = await resp.json()
    assert resp.status == 200

    assert data.keys() == {"31.01.2021", "28.02.2021"}


@pytest.mark.asyncio
async def test_wrong_date_format(cli, example_body):
    example_body['date'] = '2000.1.1'
    resp = await cli.get('/', json=example_body)

    data = await resp.json()
    assert resp.status == 400
    assert data['error'][0]['msg'] == 'invalid date format'


@pytest.mark.asyncio
async def test_wrong_period(cli, example_body):
    example_body['periods'] = 2222222
    resp = await cli.get('/', json=example_body)

    data = await resp.json()
    assert resp.status == 400

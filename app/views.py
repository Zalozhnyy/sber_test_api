from aiohttp import web
from aiohttp.web import json_response


async def index(request: web.Request) -> web.Response:
    return json_response({'text': 'hello world!'})

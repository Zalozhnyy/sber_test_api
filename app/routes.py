from aiohttp import web

from .views import calc_deposit


def setup_routes(app: web.Application) -> None:
   app.router.add_get("/", calc_deposit)

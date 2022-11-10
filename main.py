from aiohttp import web
from app.routes import setup_routes as app_setup_routes


def setup_routes(application: web.Application):
    app_setup_routes(application)


def setup_app(application: web.Application):
    setup_routes(application)


app = web.Application()

if __name__ == "__main__":
    setup_app(app)
    web.run_app(app)

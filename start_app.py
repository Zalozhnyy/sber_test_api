from aiohttp import web
from app.routes import setup_routes as app_setup_routes
from aiohttp_swagger import setup_swagger


def setup_routes(application: web.Application):
    app_setup_routes(application)


def setup_app(application: web.Application):
    setup_routes(application)


async def start_app():
    app = web.Application()
    setup_app(app)
    setup_swagger(app, swagger_url="/api/doc", ui_version=3)
    return app


if __name__ == "__main__":
    app = web.Application()
    setup_app(app)
    setup_swagger(app, swagger_url="/api/doc", ui_version=3)
    web.run_app(app, port=8080)

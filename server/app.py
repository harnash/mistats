from apistar import Include
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from apistar.backends import sqlalchemy_backend
from routers.devices import device_routes
from config import settings


routes = [
    Include('/devices', device_routes),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]

app = App(
    routes=routes,
    commands=sqlalchemy_backend.commands,
    components=sqlalchemy_backend.components,
    settings=settings
)


if __name__ == '__main__':
    app.main()

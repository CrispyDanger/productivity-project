import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "productivity-app.settings")
django_asgi_app = ASGIStaticFilesHandler(get_asgi_application())


application = ProtocolTypeRouter({
    "http": django_asgi_app,
})

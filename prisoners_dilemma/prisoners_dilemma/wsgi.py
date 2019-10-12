"""
WSGI config for prisoners_dilemma project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import eventlet
import os

from django.core.wsgi import get_wsgi_application
from socketio import WSGIApp

from website.sio import SERVER

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prisoners_dilemma.settings')

application = get_wsgi_application()

application = WSGIApp(SERVER, application)

eventlet.wsgi.server(eventlet.listen('127.0.0.1', 8001), application)
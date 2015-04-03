"""
WSGI config for Seat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys

basePath = '/var/www/capstone'

sys.path.append(basePath)
sys.path.append(basePath + '/seat')

os.environ["DJANGO_SETTINGS_MODULE"] = "seat.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

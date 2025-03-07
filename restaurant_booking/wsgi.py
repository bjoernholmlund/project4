"""
WSGI config for restaurant_booking project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os 
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

#if os.path.exists("env.py"):
#   import env # Laddar in miljövariabler

if os.path.exists(".env"):
    load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurant_booking.settings")

application = get_wsgi_application()

from .base import AUTH_USER_MODEL
from .celery import app as celery_app

__all__ = ('celery_app',)
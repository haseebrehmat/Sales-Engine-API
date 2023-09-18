from django_requests_logger.callbacks import logger as requests_logger
from functools import partial

# If you want to capture only errors (HTTP 4XX client errors and 5XX server errors), then pass only_errors argument set to True.

requests_logger_hooks = {"response": partial(requests_logger, only_errors=True)}
from django_requests_logger.models import RequestLog
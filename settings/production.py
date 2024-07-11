from settings.base import *
import rollbar
DEBUG = True
print("Production DB")
DATABASES = {
    'default': {
        'ENGINE': env("PRODUCTION_DB_ENGINE"),
        'NAME': env("PRODUCTION_DB_NAME"),
        'USER': env("PRODUCTION_DB_USER"),
        'PASSWORD': env("PRODUCTION_DB_PASSWORD"),
        'HOST': env("PRODUCTION_DB_HOST"),
        'PORT': env("PRODUCTION_DB_PORT"),
    }
}

ROLLBAR = {
    'enabled': env.bool('ROLLBAR_ENABLED', False),
    'access_token': env('ROLLBAR_ACCESS_TOKEN'),
    'environment': 'production',
    'code_version': '1.0',
    'root': BASE_DIR,
    'class': 'rollbar.logger.RollbarHandler',

}

rollbar.init(**ROLLBAR)

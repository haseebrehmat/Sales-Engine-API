from settings.base import *
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
print("Production")

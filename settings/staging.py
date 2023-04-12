from settings.base import *

DATABASES = {
    'default': {
        'ENGINE': env("STAGING_DB_ENGINE"),
        'NAME': env("STAGING_DB_NAME"),
        'USER': env("STAGING_DB_USER"),
        'PASSWORD': env("STAGING_DB_PASSWORD"),
        'HOST': env("STAGING_DB_HOST"),
        'PORT': env("STAGING_DB_PORT"),
    }
}


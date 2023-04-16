from settings.base import *
print("Development DB")
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': env("DEVELOPMENT_DB_ENGINE"),
        'NAME': env("DEVELOPMENT_DB_NAME"),
        'USER': env("DEVELOPMENT_DB_USER"),
        'PASSWORD': env("DEVELOPMENT_DB_PASSWORD"),
        'HOST': env("DEVELOPMENT_DB_HOST"),
        'PORT': env("DEVELOPMENT_DB_PORT"),
    }
}

from settings.base import *
print("Local DB")
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': env("LOCAL_DB_ENGINE"),
        'NAME': env("LOCAL_DB_NAME"),
        'USER': env("LOCAL_DB_USER"),
        'PASSWORD': env("LOCAL_DB_PASSWORD"),
        'HOST': env("LOCAL_DB_HOST"),
        'PORT': env("LOCAL_DB_PORT"),
    }
}




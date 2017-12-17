from chat_bot.settings import *
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 'd%5#py=8v@*w)5a_!6*fq$m=wt5)$il%&av=%dx-$oalh7z83e1'

NEW_INSTALLED_APPS = []

LAST_DATE = 1501569026

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': '',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost', 
        'PORT': '3306',
    }
}

BOT_MIDDLEWARES = ()

OBJECTS_TYPES = {}

INSTALLED_APPS = OLD_INSTALLED_APPS + NEW_INSTALLED_APPS
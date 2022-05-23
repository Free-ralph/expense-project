from .settings import *
import django_heroku 

ALLOWED_HOSTS = [
    'localhost', 
    'expense-project.herokuapp.com'
    ]
django_heroku.settings(locals())
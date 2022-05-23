from django.urls import path
from .views import (
    LoginView,
    register_validator,
    RegisterView,
    logout_view
    )

app_name = 'auth'
urlpatterns = [
    path('login', LoginView.as_view(), name = 'login'),
    path('logout', logout_view, name = 'logout'),
    path('register', RegisterView.as_view(), name = 'register'),
    path('register/register-validator', register_validator, name = 'field_validator'),
]
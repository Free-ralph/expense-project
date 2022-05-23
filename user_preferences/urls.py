from django.urls import path
from .views import Index

app_name = "pref"
urlpatterns = [
    path('', Index.as_view(), name = "index")
]
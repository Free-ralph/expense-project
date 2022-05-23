from django.urls import path
from .views import home_view, financial_summary

app_name = 'core'
urlpatterns = [
    path('', home_view, name = 'home'),
    path('dashboard-endpoint/', financial_summary , name = 'financial_summary')
]
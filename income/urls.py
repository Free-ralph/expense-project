from django.urls import path
from .views import (
    IncomeView,
    CreateIncomeView, 
    EditIncomeView, 
    delete_view,
    search_view, 
    income_endpoint
    )

app_name = "inc"
urlpatterns = [
    path("", IncomeView.as_view(), name = "income"),
    path("create", CreateIncomeView.as_view(), name = "create"),
    path("edit/<int:id>", EditIncomeView.as_view(), name = "edit"),
    path("delete/", delete_view, name = "delete"),
    path("search/", search_view, name = "search"),

    path("income-endpoint/", income_endpoint, name = "income_endpoint"),
]
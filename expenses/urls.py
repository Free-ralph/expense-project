from django.urls import path
from .views import (
    ExpensesView,
    CreateExpensesView, 
    EditExpensesView, 
    delete_view,
    search_view,
    add_category, 
    expense_category_summary_endpoint
    )

app_name = "exp"
urlpatterns = [
    path("", ExpensesView.as_view(), name = "expenses"),
    path("create", CreateExpensesView.as_view(), name = "create"),
    path("edit/<int:id>", EditExpensesView.as_view(), name = "edit"),
    path("delete/", delete_view, name = "delete"),
    path("search/", search_view, name = "search"),
    path("add-category/", add_category, name = "add_category"),
    path("expense-category-summary-endpoint/", expense_category_summary_endpoint, name = "expense_category_summary"),
]
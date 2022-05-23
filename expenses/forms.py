from django import forms
from .models import Expenses, Category

class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = [
            'amount',
            'description',
            'date',
            'category',
        ]

class CreateCatgoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name'
        ]
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.views import View
from .forms import ExpensesForm, CreateCatgoryForm
from .models import Category, Expenses
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .utils import paginate_qs, render_to_json
from django.template import RequestContext
import datetime
PAGINATE_BY = 4
class ExpensesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        expenses_qs = Expenses.objects.filter(owner = request.user)
        paginator_obj = paginate_qs(request, expenses_qs, PAGINATE_BY)
        context = {
            'queryset' : paginator_obj
        }
        return render(request, 'expenses/expenses.html', context)

class CreateExpensesView(LoginRequiredMixin, View):
    def get_context(self):
        category = Category.objects.all()
        context = {
            'categories' : category
        }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        return render(request, 'expenses/expense_form.html', context)    

    def post(self, request, *args, **kwargs):
        initial_data = request.POST 
        form = ExpensesForm(request.POST or None, initial = initial_data)
        if form.is_valid():
            form_instance = form.save(commit = False)
            form_instance.owner = request.user
            form_instance.save()
            messages.success(request, 'Expenses Added')
            return redirect('exp:expenses')
            
        messages.error(request, 'Invalid Form')
        context = self.get_context()   
        context['form'] = form
        
        return render(request, 'expenses/expense_form.html', context)

class EditExpensesView(LoginRequiredMixin, View):
    def get_context(self):
        category = Category.objects.all()
        context = {
            'categories' : category
        }
        return context
    def get_expense_obj(self, id):
        try :
            expense_instance = Expenses.objects.get(id = id, owner = self.request.user)
        except ObjectDoesNotExist as e:
            messages.error(request, "Sorry, this expense does not exist")
            return redirect('/')

        return expense_instance

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        id = kwargs['id']
        expense_instance = self.get_expense_obj(id)
        form = ExpensesForm(instance = expense_instance)
        context['form'] = form
        return render(request, 'expenses/expense_form.html', context)

    def post(self, request, *args, **kwargs):
        id = kwargs['id']
        expense_instance = self.get_expense_obj(id)
        form = ExpensesForm(request.POST or None, instance = expense_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated successfully")
            return redirect('exp:expenses')
        messages.error(request, "Invalid form")
        context = self.get_context()
        context['form'] = form  
        return render(request, 'expenses/expense_form.html', context)

@login_required
def delete_view(request, id=None):
    try:
        if not id:
            id = request.POST['id']
        expense_obj = Expenses.objects.get(id = id, owner = request.user)
    except ObjectDoesNotExist as e:
        messages.error(request, "Sorry, this Expense does not exist")
        return redirect('/')

    if request.POST:
        expense_obj.delete()
        messages.success(request, "Expense deleted")
    # queryset = Expenses.objects.filter(owner = request.user)
    # context = {
    #     'queryset' : queryset
    # }
    data = {
            'msg' : render_to_string('partials/messages.html', {}, request), 
            'is_deleted' : True
        }
    
    return render_to_json(request, data)

@login_required
def search_view(request):
    query = request.GET.get('query')
    #NOTE is_empty flags when the search bar has nothing in it
    queryset, is_empty = Expenses.objects.search(query)
    context = {
        'queryset' : queryset
    }
    template_name = "expenses/search_result.html"
    if request.htmx:
        template_name = 'partials/expenses/expense_table_inline.html'
        if is_empty:
            queryset = paginate_qs(request, queryset, PAGINATE_BY)
            context['queryset'] = queryset
    return render(request, template_name, context)

@login_required
def add_category(request):
    if request.POST:
        category_qs = Category.objects.all()
        form = CreateCatgoryForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            if not category_qs.filter(name__iexact = name).exists():
                form.save()
                messages.success(request, 'Category Added')
            else:
                messages.success(request, 'Already exists')
        else:
            messages.error(request, 'Invalid Form')
        context = {
            'categories' : category_qs,
        }
        data = {
            'msg' : render_to_string('partials/messages.html', {}, request), 
            'response_template' : render_to_string('partials/expenses/category_inline_form.html', context) 
        }
        
        return render_to_json(request, data)

@login_required
def expense_category_summary_endpoint(request):
    date_now = datetime.date.today()
    prev_month = date_now - datetime.timedelta(days = 31)
    prev_year = date_now - datetime.timedelta(days = 365)
    
    final_rep_year = {}
    final_rep_month = {}
    def get_expense_qs(prev_time):
        expenses_qs = Expenses.objects.filter(
                owner = request.user,
                date__gte = prev_time, date__lte = date_now 
            )
        return expenses_qs
    expense_qs_month = get_expense_qs(prev_month)
    expense_qs_year = get_expense_qs(prev_year)

    def get_category(expense):
        return expense.category

    
    category_list_month = list(set(map(get_category, expense_qs_month)))
    category_list_year = list(set(map(get_category, expense_qs_year)))
    
    def get_category_amount(category, queryset):
        amount = 0
        expense_cat_qs = queryset.filter(category__iexact = category )
        for expense in expense_cat_qs:
            amount += expense.amount
        return amount

    for category in category_list_month:
            final_rep_month[category] = get_category_amount(category, expense_qs_month)

    for category in category_list_year:
            final_rep_year[category] = get_category_amount(category, expense_qs_year)
    
    data = {
        'expenses_prev_month' : final_rep_month,
        'expenses_prev_year' : final_rep_year,
    }
    return JsonResponse(data)
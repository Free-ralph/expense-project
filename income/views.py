from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from .forms import IncomeForm
from .models import Income
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from expenses.utils import paginate_qs
import datetime
from django.template.loader import render_to_string
from expenses.utils import render_to_json

PAGINATE_BY = 5
class IncomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        income_qs = Income.objects.filter(owner = request.user)
        paginator_obj = paginate_qs(request, income_qs, PAGINATE_BY)
        context = {
            'queryset' : paginator_obj, 
        }
        return render(request, 'income/income.html', context)

class CreateIncomeView(LoginRequiredMixin,View):
    def get_context(self):
        context = {}
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        return render(request, 'income/income_form.html', context)    

    def post(self, request, *args, **kwargs):
        initial_data = request.POST 
        form = IncomeForm(request.POST or None, initial = initial_data)
        if form.is_valid():
            form_instance = form.save(commit = False)
            form_instance.owner = request.user
            form_instance.save()
            messages.success(request, 'Income Added')
            return redirect('inc:income')
            
        messages.error(request, 'Invalid Form')
        context = self.get_context()   
        context['form'] = form
        
        return render(request, 'income/income_form.html', context) 

class EditIncomeView(View):
    def get_context(self):
        context = {}
        return context
    def get_income_obj(self, id):
        try :
            income_instance = Income.objects.get(id = id, owner = self.request.user)
        except ObjectDoesNotExist as e:
            messages.error(request, "Sorry, this income does not exist")
            return redirect('/')

        return income_instance

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        id = kwargs['id']
        income_instance = self.get_income_obj(id)
        form = IncomeForm(instance = income_instance)
        context['form'] = form
        return render(request, 'income/income_form.html', context)

    def post(self, request, *args, **kwargs):
        id = kwargs['id']
        income_instance = self.get_income_obj(id)
        form = IncomeForm(request.POST or None, instance = income_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated successfully")
            return redirect('inc:income')
        messages.error(request, "Invalid form")
        context = self.get_context()
        context['form'] = form  
        return render(request, 'income/income_form.html', context)


def delete_view(request, id=None):
    try:
        if not id:
            id = request.POST['id']
        income_obj = Income.objects.get(id = id, owner = request.user)
    except ObjectDoesNotExist as e:
        messages.error(request, "Sorry, this Income does not exist")
        return redirect('/')

    if request.POST:
        income_obj.delete()
        messages.success(request, "Income deleted")
    queryset = Income.objects.filter(owner = request.user)
    context = {
        'queryset' : queryset
    }
    data = {
            'msg' : render_to_string('partials/messages.html', {}, request), 
            'is_deleted' : True
        }
    
    return render_to_json(request, data)
    # return render(request, 'partials/income/income_table_inline.html', context)


def search_view(request):
    query = request.GET.get('query')
    #NOTE is_empty flags when the search bar has nothing in it
    queryset, is_empty = Income.objects.search(query)
    context = {
        'queryset' : queryset
    }
    template_name = "income/search_result.html"
    if request.is_ajax:
        template_name = 'partials/income/income_table_inline.html'
        if is_empty:
            queryset = paginate_qs(request, queryset, PAGINATE_BY)
            context['queryset'] = queryset
    return render(request, template_name, context)


@login_required
def income_endpoint(request):
    date_now = datetime.date.today()
    
    def get_amount(prev, date_now):
        amount = 0
        qs = Income.objects.filter(date__gte = prev, date__lte = date_now)
        for item in qs:
            amount += item.amount
        return amount

    def get_prev_week(date_now):
        days_of_the_week = {
            1 : 'Tuesday' ,
            2 : 'Wednesday' ,
            3 : 'Thursday' ,
            4 : 'Friday',
            5 : 'Saturday',
            6 : 'Sunday',
            0 : 'Monday',
        }

        today = datetime.date.today().weekday()
        prev_week_analysis = {}
        for i in range(1, 8):
            prev_day = date_now - datetime.timedelta(days = 1)
            prev_week_analysis[days_of_the_week[today]] = get_amount(prev_day, date_now)
            date_now = prev_day
            today = date_now.weekday()

        return prev_week_analysis

    def get_prev_year(date_now):
        # for the past year
        current_month = datetime.datetime.now().month
        month_name = datetime.datetime.strptime(str(current_month), "%m").strftime('%B')
        prev_month_analysis = {}
        
        for i in range(12):
            prev_month = date_now - datetime.timedelta(days = 30)
            prev_month_analysis[month_name] = get_amount(prev_month, date_now)
            date_now = prev_month
            current_month = date_now.month
            month_name = datetime.datetime.strptime(str(current_month), "%m").strftime('%B') 

        return prev_month_analysis


    
    data = {
        'prev_week_analysis' : get_prev_week(date_now),
        'prev_month_analysis' : get_prev_year(date_now),
    }
    return JsonResponse(data)
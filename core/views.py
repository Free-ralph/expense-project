from django.shortcuts import render
from expenses.models import Expenses
from income.models import Income
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import datetime

@login_required
def home_view(request):
    date_now = datetime.date.today()
    today = date_now - datetime.timedelta(hours = 24)
    prev_month = date_now - datetime.timedelta(days = 31)
    prev_week = date_now - datetime.timedelta(days = 7)
    prev_year = date_now - datetime.timedelta(days = 365)

    def get_summary(time):
        income = Income.objects.time_amount_filter(time)
        expense = Expenses.objects.time_amount_filter(time)
        total_amount = income['amount'] - expense['amount']
        total_transactional_count = income['queryset'].count() + expense['queryset'].count()
        return {
            'amount' : total_amount,
            'count' : total_transactional_count
        }
    
    todays_summary = get_summary(today)
    prev_week_summary =  get_summary(prev_week)
    prev_month_summary =  get_summary(prev_month)
    prev_year_summary =  get_summary(prev_year)

    context = {
        'todays_summary' : todays_summary,
        'prev_week_summary' : prev_week_summary,
        'prev_month_summary' : prev_month_summary,
        'prev_year_summary' : prev_year_summary,
    }
    return render(request, 'core/home.html', context)


@login_required
def financial_summary(request):
    date_now = datetime.date.today()
    
    def get_amount(prev, date_now):
        amount = 0
        income_qs = Income.objects.filter(date__gte = prev, date__lte = date_now)
        expense_qs = Expenses.objects.filter(date__gte = prev, date__lte = date_now)

        for item in income_qs:
            amount += item.amount
        for item in expense_qs:
            amount -= item.amount
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
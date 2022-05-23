from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import UserPreference
from django.views import View
from django.views.generic import DetailView
from .forms import CurrencyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from moneyed import CURRENCIES
from django.contrib import messages

class Index(LoginRequiredMixin, View):

    def get_context_data(self):
        # NOTE this is not defined in the View Class
        context = {
            'currencies' : self.get_currencies() 
        }
        
        return context


    @staticmethod
    def get_currencies():
        '''
            returns an array of dictionaries containing all the currencies 
        '''


        currency_data = []
        for currency_code in CURRENCIES:
            currency_data.append(
                {
                    'name' : CURRENCIES[currency_code].name,
                    'value' : currency_code
                }
            )

        return currency_data
    
    def get_current_currency(self, currency = None):
        '''
            this gets the user's current currency
            returns the defualt if teh user hasn't choosen any yet
        '''

        if currency:
            name = CURRENCIES[currency].name
            value = currency
        else:
            value = self.request.user.user_preference.currency
            name = CURRENCIES[value].name

        current_currency = {
            'name' : name,
            'value' : value
        }
        return current_currency

    def get(self, request, *args, **kwargs):
        try:
            user_pref = UserPreference.objects.get(user = request.user)
        except:
            UserPreference.objects.create(user = request.user)
        value, name = self.get_current_currency()
        
        context = self.get_context_data()
        context['current_currency'] = self.get_current_currency()
        return render(request, 'preferences/index.html', context)

    def post(self, request, *args, **kwargs):
        form = CurrencyForm(request.POST or None)
        template_name = "preferences/index.html"
        if form.is_valid():
            currency = form.cleaned_data.get('currency')
            try:
                user_preference = UserPreference.objects.get(user = request.user)
            except ObjectDoesNotExist :
                user_preference = UserPreference(user = request.user)
            user_preference.currency = currency 
            user_preference.save()
            messages.success(request, "currency updated successfully")
            if request.htmx:
                template_name = 'partials/preferences/currency_form.html'
        else:
            messages.success(request, "form invalid")
        context = self.get_context_data()
        context['current_currency'] = self.get_current_currency(currency = currency)
        return render(request, template_name , context)
    

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.views import View
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.http import JsonResponse

# Create your views here.

class LoginView(View):
    def get(self, request,  *args, **kwargs):
        form = AuthenticationForm()

        context = {
            'form' : form
        }
        return render(request, 'authentication/login.html', context)
    
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data =request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = form.get_user()
            print(user)
            login(request, user)
            messages.success(request, f'welcome! {username}')
            return redirect('core:home')
        messages.error(request, 'username or password don\'t match')
        context = {
            'form' : form, 
            'show_message' : True
        }
        print(form.errors)
        return render(request, 'authentication/login.html', context)

def logout_view(request):

    if request.POST:
        response = request.POST.get('response')
        if response == "yes":
            if request.user:
                logout(request)
                messages.success(request, 'logged out successfully')
                ajax = request.POST.get('ajax')
                if ajax == "true": 
                    url = reverse("auth:login")
                    return JsonResponse({'url' : url})
                return redirect('auth:login')
        else :
            return redirect("/")
        messages.warning(request, 'you have already been logged out')
        return redirect('/')
    context = {
        'show_message' : True
    }
    return render(request, 'authentication/confirm_logout.html', context)

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form =  RegisterForm()
        context = {
            'form' : form
        }
        return render(request, 'authentication/register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            name_list = str(name).split(' ')
            fullname = " ".join(name_list)
            form_instance = form.save(commit=False)
            form_instance.first_name = fullname
            form_instance.Email_address = email
            # form_instance.is_active = False
            form_instance.set_password(form_instance.password)
            form_instance.save()
            # subject = f"Hello{name}Activate you account"
            # body = ""
            # email = EmailMessage(
            #     subject , 
            #     body, 
                
            # )
            messages.success(request, 'regstration was successfull, please login')
            return redirect('auth:login')
        messages.error(request, 'form invalid')
        context = {
            'form' : form,
            'form_data' : request.POST, 
            'show_message' : True
        }
        return render(request, 'authentication/register.html', context)

def register_validator(request):
    name = request.GET.get('name')
    value = request.GET.get('value')
    data = {}
    print(name, value)
    if name == "username":
        if value == "" or value is None:
            data = {"error" : "This field is required"}
        elif not str(value).isalnum():
            data = {"error" : "you must use only alphanumerics"}
        elif User.objects.filter(username__iexact = value).exists():
            data = {"error" : "username already in use"}
        else :
            data = {'valid' : True}
    elif name == 'email' :
        if value == "" or value is None:
            data = {"error" : "This field is required"}
        elif not validate_email(str(value)):
            data = {"error" : "email not in the proper format"}
        elif User.objects.filter(email__iexact = value).exists():
            data = {"error" : "email already in use"}
        else :
            data = {'valid' : True}
    elif name == "password" : 
        try:
            validate_password(value)
        except ValidationError as e:
            data = {'error' : ' '.join(e.messages)}
        else:
            data = {'valid' : True}
    else:
        data = {'error' :"No field given"}
    return JsonResponse(data)

import requests
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from converter.forms import CustomUserCreationForm, CustomAuthenticationForm


def index(request):
    response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
    currencies = response.json()['rates']
    if request.method == 'GET':
        context = {'currencies': currencies}
        return render(request, 'converter/home.html', context)
    elif request.method == 'POST':
        from_amount = float(request.POST.get('from-amount'))
        from_curr = request.POST.get('from-curr')
        to_curr = request.POST.get('to-curr')
        converted_amount = round((currencies[to_curr] / currencies[from_curr]) * from_amount, 2)
        context = {
            'currencies': currencies,
            'from_amount': from_amount,
            'from_curr': from_curr,
            'to_curr': to_curr,
            'converted_amount': converted_amount,
        }
        return render(request, 'converter/home.html', context=context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            username = User.objects.get(email=email).username
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})




def user_logout(request):
    logout(request)
    return redirect('/')
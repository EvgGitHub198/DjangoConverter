import requests
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/')
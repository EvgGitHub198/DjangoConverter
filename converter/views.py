import requests
from django.shortcuts import render


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
        return render(request, 'converter/home.html', context)

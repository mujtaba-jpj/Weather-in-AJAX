from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import requests
import datetime



def test(keys, values):
    return dict(zip(keys, values))


def weather(request):
    if request.method == 'POST':
        search_query = request.POST['search_query']

        url = 'http://api.weatherapi.com/v1/forecast.json'

        params = {
            'key': 'e4e3a794b6c6401bbaf183116231703',
            'q': search_query,
            'days': '4',
        }

        data = requests.request("GET", url, params=params)


        # error forwarding 
        if data.status_code == 400:
            return JsonResponse({'status': 2})

        data = data.json()
        # current day
        dt = datetime.datetime.fromtimestamp(
            data['location']['localtime_epoch'])
        day = dt.strftime('%A')
        # 4 days ahead
        # Replace with your starting date
        start_date = datetime.date(dt.year, dt.month, dt.day)

        forecast_days_name = []
        forecastdata = []
        # Loop over the next 4 days
        for i in range(1, 4):
            # Get the date of the current day
            current_date = start_date + datetime.timedelta(days=i)

            # Get the name of the current day
            day_name = current_date.strftime('%a')
            forecast_days_name.append(day_name)

        for forecast_data in data['forecast']['forecastday']:
            forecastdata.append(forecast_data['day']['avgtemp_c'])

        forecast = test(forecast_days_name, forecastdata)

        context = {'search_query': search_query, 'data': data,
               'day': day, 'forecast': forecast}
        
        return JsonResponse({'status': 1,'context' : context })


    else:
        return JsonResponse({'status': 0})



def home(request):
    
    url = 'http://api.weatherapi.com/v1/forecast.json'

    params = {
        'key': 'e4e3a794b6c6401bbaf183116231703',
        'q': 'Karachi',
        'days': '4',
    }

    data = requests.request("GET", url, params=params)

    data = data.json()
    # current day
    dt = datetime.datetime.fromtimestamp(
        data['location']['localtime_epoch'])
    day = dt.strftime('%A')
    # 4 days ahead
    # Replace with your starting date
    start_date = datetime.date(dt.year, dt.month, dt.day)

    forecast_days_name = []
    forecastdata = []
    # Loop over the next 4 days
    for i in range(1, 4):
        # Get the date of the current day
        current_date = start_date + datetime.timedelta(days=i)

        # Get the name of the current day
        day_name = current_date.strftime('%a')
        forecast_days_name.append(day_name)

    for forecast_data in data['forecast']['forecastday']:
        forecastdata.append(forecast_data['day']['avgtemp_c'])

    forecast = test(forecast_days_name, forecastdata)
    
    context = {'data': data, 'day': day, 'forecast': forecast}
    return render(request, 'weather.html', context)

# def weather(request):
#     if request.method == 'POST':
#         return JsonResponse({'status': 'Save','test' : request.POST })

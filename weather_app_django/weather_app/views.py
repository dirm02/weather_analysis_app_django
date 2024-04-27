from django.shortcuts import render
import requests
from django.http import JsonResponse
from .forms import ZipCodeForm, StartDateForm, EndDateForm
from datetime import datetime

BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
API_KEY = '3KAJKHWT3UEMRQWF2ABKVVVZE'

# Create your views here.
def get_weather(request):
    dates = []
    temperatures = []
    humidities = []
    precipitations = []
    wind_speeds = []

    if request.method == 'POST':
        location_form = ZipCodeForm(request.POST)
        startDate_form = StartDateForm(request.POST)
        endDate_form = EndDateForm(request.POST)
        print(location_form)
        print(location_form.cleaned_data)
        if location_form.is_valid() and startDate_form.is_valid() and endDate_form.is_valid():
            location = location_form.cleaned_data['zip_code']
            start_date = startDate_form.cleaned_data['start_date']
            end_date = endDate_form.cleaned_data['end_date']
            if end_date:
                url = f"{BASE_URL}{location}/{start_date}/{end_date}?key={API_KEY}"
            elif start_date:
                url = f"{BASE_URL}{location}/{start_date}?key={API_KEY}"
            else:
                url = f"{BASE_URL}{location}?key={API_KEY}"
            try:
                response = requests.get(url)
                weather_data = response.json()
                print('weather')
                print(weather_data)

                days = weather_data['days']
                dates = [datetime.strptime(day['datetime'], '%Y-%m-%d') for day in days]
                temperatures = [day.get('temp', None) for day in days]
                humidities = [day.get('humidity', None) for day in days]
                precipitations = [day.get('precip', None) for day in days]
                wind_speeds = [day.get('windspeed', None) for day in days]
                
                # response.raise_for_status()
                # return response.json()
                # return JsonResponse({'status': 'success', 'payload': weather})
            except requests.RequestException as e:
                print('error', e)
                # return JsonResponse({'status': 'fail', 'message': e}, status = 500)
    else:
        location_form = ZipCodeForm()
        startDate_form = StartDateForm()
        endDate_form = EndDateForm()
        
    context= {
        'dates': dates,
        'temperatures': temperatures,
        'humidities': humidities,
        'precipitations': precipitations,
        'wind_speeds': wind_speeds,
        'location_form' : location_form,
        'startDate_form' : startDate_form,
        'endDate_form' : endDate_form,
    }
    
    return render(request, 'weather_dashboard/weather_main.html', context)
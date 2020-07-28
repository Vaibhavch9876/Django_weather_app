from django.shortcuts import render, HttpResponse
import requests
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=db252c4b58614075cd4bae1c2002c319'
    cities = City.objects.all()

    if request.method == 'POST':
        form = CityForm(request.POST)
        data_form = form.save(commit=False)
        city_name = form.cleaned_data['name']
        if City.objects.get(name=city_name):
            pass
        else:
            form.name = url.format(city_name)
            form.save()

    form = CityForm()
    weather_data = []

    for city in cities:

        city_weather = requests.get(url.format(city)).json()

        if city_weather['cod'] != 200:
            City.objects.get(name=city).delete()

            continue

        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }

        weather_data.append(weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/index.html', context)


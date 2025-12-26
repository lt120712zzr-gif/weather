from django.shortcuts import render
from models import *
# Create your views here.

def index(request):
    return render(request,'index.html')

def cityChar(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    cites = getGlobalData()
    city = request.GET.get('city') or cites[0]
    print(city)
    date, maxTemp, minTemp = getCityMinMaxTemp(city)
    resultWeather = getWeatherListByCity(city)
    resultWind = getWindListByCity(city)
    resultWindOrder = getWindOrderListByCity(city)

    return render(request, template_name='cityChar.html', context={
        'userInfo': userInfo,
        'cites': cites,
        'defaultCity': city,
        'date': date,
        'maxTemp': maxTemp,
        'minTemp': minTemp,
        'resultWeather': resultWeather[:15],
        'resultWind': resultWind,
        'resultWindOrder': resultWindOrder,
    })
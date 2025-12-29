from django.shortcuts import render,redirect
from models import *
from utils import *
from utils.getChartData import *
# Create your views here.

def index(request):
    uname = request.session.get('username')
    userInfo =User.objects.get(username=uname)
    dateList=getDateList()
    defaultDate=request.GET.get('date') or dateList[0]
    cites=getGlobalData()
    city=request.GET.get('city') or cites[0]
    dataList=getMapData()
    return render(request,'index.html',{
        'userInfo':userInfo,
        'dateList':dateList,
        'defaultDate':defaultDate,
        'dataList':dataList,
        'cites':cites,
    })

def cityChar(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    cites = getGlobalData()
    city = request.GET.get('city') or cites[0]
    print(city)
    date, maxTemp, minTemp = getCityMaxMinTemp(city)
    resultWeather = getWeatherListByCity(city)
    resultWind = getWindListByCity(city)
    resultWindOrder = getWindOrderListByCity(city)

    return render(request, 'cityChar.html', {
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

def tableData(request):
    uname = request.session.get('username')
    userinfo = User.objects.get(username=uname)
    cites = getGlobalData()
    city = request.GET.get("city") or cites[0]
    print(city)
    tableData = list(getTableData(city))
    return render(request, 'tableData.html', {
        "userinfo": userinfo,
        "cites": cites,
        "defaultCity": city,
        "tableData": tableData
    })
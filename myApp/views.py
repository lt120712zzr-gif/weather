from django.shortcuts import render,redirect
from .models import *
from utils import *
from utils.getChartData import *
from django.http import JsonResponse
# Create your views here.

def index(request):
    uname = request.session.get('username')
    userInfo = None
    if uname:
        try:
            userInfo = User.objects.get(username=uname)
        except User.DoesNotExist:
            pass

    dateList = getDateList()
    defaultDate = request.GET.get('date') or (dateList[0] if dateList else '')
    cites = getGlobalData()
    city = request.GET.get('city') or (cites[0] if cites else '')
    dataList = getMapData(defaultDate)
    print(f'dateList: {dateList}, defaultDate: {defaultDate}, dataList: {dataList}')
    return render(request,'index.html',{
        'userInfo': userInfo,
        'dateList': dateList,
        'defaultDate': defaultDate,
        'dataList': dataList,
        'cites': cites,
    })

def cityChar(request):
    uname = request.session.get('username')
    if not uname:
        return render(request, 'cityChar.html')
    try:
        userInfo = User.objects.get(username=uname)
    except User.DoesNotExist:
        return render(request, 'cityChar.html')
        return
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
    if not uname:
        return render(request, 'tableData.html')
    try:
        userinfo = User.objects.get(username=uname)
    except User.DoesNotExist:
        return render(request, 'tableData.html')
        return
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

def map_data_api(request):
    """API接口：返回指定日期的地图数据（JSON格式）"""
    date = request.GET.get('date')
    print(f'API请求日期: {date}')
    if not date:
        # 如果没有指定日期，返回默认日期的数据
        dateList = getDateList()
        date = dateList[0] if dateList else ''

    dataList = getMapData(date)
    print(f'API返回数据: {dataList}')
    return JsonResponse({
        'success': True,
        'date': date,
        'data': dataList
    }, safe=False)
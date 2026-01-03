from django.shortcuts import render,redirect
from .models import *
from utils import *
from utils.getChartData import *
from django.http import JsonResponse
from django.db.models import Q, Count
from django.contrib import messages
import hashlib
from functools import wraps
# Create your views here.


def login_required(view_func):
    """登录验证装饰器"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        username = request.session.get('username')
        if not username:
            return redirect('/login')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
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
    # print(f'dateList: {dateList}, defaultDate: {defaultDate}, dataList: {dataList}')
    return render(request,'index.html',{
        'userInfo': userInfo,
        'dateList': dateList,
        'defaultDate': defaultDate,
        'dataList': dataList,
        'cites': cites,
    })

@login_required
def cityChar(request):
    cites = getGlobalData()
    city = request.GET.get('city') or (cites[0] if cites else '')
    # print(city)
    date, maxTemp, minTemp = getCityMaxMinTemp(city)
    resultWeather = getWeatherListByCity(city)
    resultWind = getWindListByCity(city)
    resultWindOrder = getWindOrderListByCity(city)
    userInfo = None
    uname = request.session.get('username')
    if uname:
        try:
            userInfo = User.objects.get(username=uname)
        except User.DoesNotExist:
            pass

    return render(request, 'cityChar.html', {
        'userInfo': userInfo,
        'cites': cites,
        'defaultCity': city,
        'date': date,
        'maxTemp': maxTemp,
        'minTemp': minTemp,
        'resultWeather': resultWeather,
        'resultWind': resultWind,
        'resultWindOrder': resultWindOrder,
    })

@login_required
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

@login_required
def dataVisualization(request):
    """数据可视化页面 - 支持温度和空气质量统计"""
    cites = getGlobalData()
    monthList = getMonthList()
    defaultMonth = request.GET.get('month') or (monthList[0] if monthList else '2023-01')
    vizType = request.GET.get('type', 'temp')  # 默认显示温度统计，可选 'temp' 或 'air'

    # 获取所有城市
    cityNames = cites[:20]  # 限制显示前20个城市

    # 对于温度类型，先检查哪些城市有数据
    if vizType == 'temp':
        monthData = list(WeatherInfo.objects.filter(
            date__startswith=defaultMonth,
            city__in=cityNames
        ).values('city', 'mastHeightDay', 'mastSmallDay'))
        # 获取有数据的城市
        citiesWithData = set([item['city'] for item in monthData if item['mastHeightDay'] or item['mastSmallDay']])
        # 只保留有数据的城市
        cityNames = [city for city in cityNames if city in citiesWithData]
    # 对于空气质量类型，先检查哪些城市有数据
    elif vizType == 'air':
        monthData = list(WeatherInfo.objects.filter(
            date__startswith=defaultMonth,
            city__in=cityNames
        ).values('city', 'mastAir', 'lostAir', 'averageAir'))
        # 获取有数据的城市
        citiesWithData = set([item['city'] for item in monthData if item['mastAir'] or item['lostAir'] or item['averageAir']])
        # 只保留有数据的城市
        cityNames = [city for city in cityNames if city in citiesWithData]

    # 初始化数据
    averageHighTemps = []
    averageLowTemps = []
    extremeHighTemps = []
    extremeLowTemps = []

    # 空气质量数据
    maxAirQualities = []
    minAirQualities = []
    avgAirQualities = []

    if vizType == 'temp':
        # 温度统计数据
        for city in cityNames:
            cityData = [item for item in monthData if item['city'] == city]
            if cityData:
                # 计算平均温度
                highTemps = [float(item['mastHeightDay']) for item in cityData if item['mastHeightDay'] and item['mastHeightDay'].strip()]
                lowTemps = [float(item['mastSmallDay']) for item in cityData if item['mastSmallDay'] and item['mastSmallDay'].strip()]

                avgHigh = sum(highTemps) / len(highTemps) if highTemps else 0
                avgLow = sum(lowTemps) / len(lowTemps) if lowTemps else 0

                averageHighTemps.append(round(avgHigh, 1))
                averageLowTemps.append(round(avgLow, 1))

                # 计算极端温度
                extremeHigh = max(highTemps) if highTemps else 0
                extremeLow = min(lowTemps) if lowTemps else 0

                extremeHighTemps.append(round(extremeHigh, 1))
                extremeLowTemps.append(round(extremeLow, 1))
            else:
                averageHighTemps.append(0)
                averageLowTemps.append(0)
                extremeHighTemps.append(0)
                extremeLowTemps.append(0)
    else:
        # 空气质量统计数据
        for city in cityNames:
            cityData = [item for item in monthData if item['city'] == city]
            if cityData:
                # 收集最高和最低空气质量数据
                maxAirValues = []
                minAirValues = []
                avgAirValues = []

                for item in cityData:
                    # 最高空气质量
                    if item['mastAir'] and item['mastAir'].strip():
                        try:
                            aqi = float(item['mastAir'])
                            maxAirValues.append(aqi)
                        except:
                            pass
                    # 最低空气质量
                    if item['lostAir'] and item['lostAir'].strip():
                        try:
                            aqi = float(item['lostAir'])
                            minAirValues.append(aqi)
                        except:
                            pass
                    # 平均空气质量
                    if item['averageAir'] and item['averageAir'].strip():
                        try:
                            aqi = float(item['averageAir'])
                            avgAirValues.append(aqi)
                        except:
                            pass

                # 计算最高和最低
                maxAir = max(maxAirValues) if maxAirValues else 0
                minAir = min(minAirValues) if minAirValues else 0
                avgAir = sum(avgAirValues) / len(avgAirValues) if avgAirValues else 0

                maxAirQualities.append(round(maxAir, 1))
                minAirQualities.append(round(minAir, 1))
                avgAirQualities.append(round(avgAir, 1))
            else:
                maxAirQualities.append(0)
                minAirQualities.append(0)
                avgAirQualities.append(0)

    userInfo = None
    uname = request.session.get('username')
    if uname:
        try:
            userInfo = User.objects.get(username=uname)
        except User.DoesNotExist:
            pass

    return render(request, 'dataVisualization.html', {
        'userInfo': userInfo,
        'cites': cites,
        'defaultMonth': defaultMonth,
        'monthList': monthList,
        'vizType': vizType,
        'cityNames': cityNames,
        'averageHighTemps': averageHighTemps,
        'averageLowTemps': averageLowTemps,
        'extremeHighTemps': extremeHighTemps,
        'extremeLowTemps': extremeLowTemps,
        'maxAirQualities': maxAirQualities,
        'minAirQualities': minAirQualities,
        'avgAirQualities': avgAirQualities,
    })

@login_required
def detailInfo(request):
    """详情信息页面 - 支持分页、排序、搜索"""
    cites = getGlobalData()
    defaultCity = request.GET.get('city') or (cites[0] if cites else '')

    # 获取分页参数
    currentPage = int(request.GET.get('page', 1))
    pageSize = int(request.GET.get('pageSize', 20))

    # 获取排序参数
    sortField = request.GET.get('sortField', 'date')
    sortOrder = request.GET.get('sortOrder', 'desc')

    # 获取搜索参数
    searchQuery = request.GET.get('search', '').strip()
    monthQuery = request.GET.get('month', '').strip()
    dateNumQuery = request.GET.get('date', '').strip()

    # 构建查询
    query = Q(city=defaultCity)

    # 添加月份过滤
    if monthQuery:
        query &= Q(date__startswith=monthQuery)

    # 添加日期过滤（只匹配日期数字，如输入15，匹配15号的数据）
    if dateNumQuery:
        # 假设日期格式为 YYYY-MM-DD，我们需要匹配 DD 部分
        query &= Q(date__endswith='-' + dateNumQuery.zfill(2) if len(dateNumQuery) == 1 else dateNumQuery)

    # 添加搜索条件（搜索多个字段）
    if searchQuery:
        search_fields = ['date', 'weekDay', 'wearther', 'wind', 'windOrder',
                      'averageHeight', 'averageSmall', 'mastHeight', 'mastSmall', 'averageAir', 'mastAir', 'lostAir']
        search_query = Q()
        for field in search_fields:
            search_query |= Q(**{f"{field}__icontains": searchQuery})
        query &= search_query

    # 获取数据
    weatherData = WeatherInfo.objects.filter(query)

    # 统计总数（在排序和分页之前）
    totalCount = weatherData.count()

    # 排序 - 针对温度字段转换为数值排序
    valid_fields = ['date', 'weekDay', 'wearther', 'mastHeightDay', 'mastSmallDay', 'wind', 'windOrder',
                  'averageHeight', 'averageSmall', 'mastHeight', 'mastSmall', 'averageAir', 'mastAir', 'lostAir']
    if sortField in valid_fields:
        order_prefix = '-' if sortOrder == 'desc' else ''
        # 所有温度/数值字段都需要转换为数值排序
        numeric_fields = ['mastHeightDay', 'mastSmallDay', 'averageHeight', 'averageSmall',
                      'mastHeight', 'mastSmall', 'averageAir', 'mastAir', 'lostAir']
        if sortField in numeric_fields:
            if sortOrder == 'desc':
                weatherData = sorted(weatherData, key=lambda x: float(getattr(x, sortField)) if getattr(x, sortField) else 0, reverse=True)
            else:
                weatherData = sorted(weatherData, key=lambda x: float(getattr(x, sortField)) if getattr(x, sortField) else 0, reverse=False)
        else:
            weatherData = weatherData.order_by(f'{order_prefix}{sortField}')

    # 分页
    start = (currentPage - 1) * pageSize
    end = start + pageSize
    tableData = weatherData[start:end]

    # 计算总页数
    totalPages = (totalCount + pageSize - 1) // pageSize

    userInfo = None
    uname = request.session.get('username')
    if uname:
        try:
            userInfo = User.objects.get(username=uname)
        except User.DoesNotExist:
            pass

    return render(request, 'detailInfo.html', {
        'userInfo': userInfo,
        'cites': cites,
        'defaultCity': defaultCity,
        'tableData': tableData,
        'currentPage': currentPage,
        'pageSize': pageSize,
        'totalCount': totalCount,
        'totalPages': totalPages,
        'sortField': sortField,
        'sortOrder': sortOrder,
        'searchQuery': searchQuery,
        'monthQuery': monthQuery,
        'dateQuery': dateNumQuery,
        'monthList': getMonthList(),
    })

@login_required
def wordCloud(request):
    """天气词云图页面"""
    cites = getGlobalData()
    defaultCity = request.GET.get('city') or (cites[0] if cites else '')

    # 获取天气数据统计 - 使用values直接统计，减少数据库查询
    weatherCount = WeatherInfo.objects.filter(
        city=defaultCity,
        wearther__isnull=False
    ).exclude(wearther='').values('wearther').annotate(
        count=Count('wearther')
    )

    # 转换为词云格式
    wordCloudData = [{'name': item['wearther'], 'value': item['count']} for item in weatherCount]

    # 按数量排序，取前50个
    wordCloudData = sorted(wordCloudData, key=lambda x: x['value'], reverse=True)[:50]

    userInfo = None
    uname = request.session.get('username')
    if uname:
        try:
            userInfo = User.objects.get(username=uname)
        except User.DoesNotExist:
            pass

    return render(request, 'wordCloud.html', {
        'userInfo': userInfo,
        'cites': cites,
        'defaultCity': defaultCity,
        'wordCloudData': wordCloudData,
    })


@login_required
def weatherForecast(request):
    """天气预测页面"""
    cites = getGlobalData()
    defaultCity = request.GET.get('city') or (cites[0] if cites else '')

    # 获取该城市所有历史天气数据
    allWeather = list(WeatherInfo.objects.filter(
        city=defaultCity,
        wearther__isnull=False
    ).exclude(wearther='').values('date', 'mastHeightDay', 'mastSmallDay', 'wearther', 'wind', 'weekDay').order_by('date'))

    # 基于历史同期数据预测今天和未来7天
    forecastData = []
    from datetime import datetime, timedelta

    # 从今天开始预测
    today = datetime.now()
    startDate = today

    # 预测8天（包含今天）
    days = 8
    for i in range(days):
        futureDate = startDate + timedelta(days=i)
        dateStr = futureDate.strftime('%Y-%m-%d')
        futureMonth = futureDate.month
        futureDay = futureDate.day

        # 找到历史上相同月份和日期的数据（历年同期）
        sameDateWeather = []
        weatherTypes = {}
        winds = {}

        for weather in allWeather:
            try:
                weatherDate = datetime.strptime(weather['date'], '%Y-%m-%d')
                # 匹配相同月和日
                if weatherDate.month == futureMonth and weatherDate.day == futureDay:
                    sameDateWeather.append(weather)

                    # 统计天气类型频率
                    wtype = weather['wearther']
                    if wtype:
                        weatherTypes[wtype] = weatherTypes.get(wtype, 0) + 1

                    # 统计风向频率
                    windDir = weather['wind']
                    if windDir:
                        winds[windDir] = winds.get(windDir, 0) + 1
            except:
                continue

        # 如果没有同期数据，使用最近30天数据作为备选
        if not sameDateWeather:
            sameDateWeather = allWeather[-30:] if len(allWeather) >= 30 else allWeather

            for weather in sameDateWeather:
                try:
                    wtype = weather['wearther']
                    if wtype:
                        weatherTypes[wtype] = weatherTypes.get(wtype, 0) + 1

                    windDir = weather['wind']
                    if windDir:
                        winds[windDir] = winds.get(windDir, 0) + 1
                except:
                    continue

        # 计算同期平均高温和低温
        avgHigh = 0
        avgLow = 0
        count = 0

        for weather in sameDateWeather:
            try:
                high = float(weather['mastHeightDay']) if weather['mastHeightDay'] else 0
                low = float(weather['mastSmallDay']) if weather['mastSmallDay'] else 0
                avgHigh += high
                avgLow += low
                count += 1
            except:
                continue

        if count > 0:
            avgHigh = round(avgHigh / count, 1)
            avgLow = round(avgLow / count, 1)
        else:
            avgHigh = 25
            avgLow = 15

        # 选择出现频率最高的天气类型
        predictedWeather = '多云'
        if weatherTypes:
            predictedWeather = max(weatherTypes.items(), key=lambda x: x[1])[0]

        # 选择出现频率最高的风向
        predictedWind = '无风'
        if winds:
            predictedWind = max(winds.items(), key=lambda x: x[1])[0]

        # 今日显示今日标记
        isToday = (i == 0)

        # 星期名称
        dayOfWeek = futureDate.weekday()  # 0=周一, 6=周日
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekdayName = weekdays[dayOfWeek]

        forecastData.append({
            'date': dateStr,
            'weekDay': '今日' if isToday else weekdayName,
            'high': avgHigh,
            'low': avgLow,
            'weather': predictedWeather,
            'wind': predictedWind,
            'isToday': isToday
        })

    userInfo = None
    uname = request.session.get('username')
    if uname:
        try:
            userInfo = User.objects.get(username=uname)
        except User.DoesNotExist:
            pass

    return render(request, 'weatherForecast.html', {
        'userInfo': userInfo,
        'cites': cites,
        'defaultCity': defaultCity,
        'forecastData': forecastData,
    })


def login_view(request):
    """登录页面"""
    # 清除所有旧消息
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 简单的密码加密（实际项目应使用更安全的方式）
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        try:
            user = User.objects.get(username=username)
            if user.password == hashed_password:
                # 登录成功，保存session
                request.session['username'] = username
                messages.success(request, '登录成功！')
                return redirect('index')
            else:
                messages.error(request, '用户名或密码错误！')
        except User.DoesNotExist:
            messages.error(request, '用户不存在！')

    return render(request, 'pages-login.html')


def register_view(request):
    """注册页面"""
    # 清除所有旧消息
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在！')
            return render(request, 'pages-register.html')

        # 简单的密码加密
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        # 创建用户
        User.objects.create(
            username=username,
            password=hashed_password
        )

        messages.success(request, '注册成功！请登录')
        return redirect('login')

    return render(request, 'pages-register.html')


def logout_view(request):
    """登出"""
    if 'username' in request.session:
        del request.session['username']
    return redirect('login')


@login_required
def profile_view(request):
    """个人信息页面"""
    uname = request.session.get('username')
    try:
        userInfo = User.objects.get(username=uname)
    except User.DoesNotExist:
        return redirect('login')

    if request.method == 'POST':
        newPassword = request.POST.get('newPassword')
        confirmPassword = request.POST.get('confirmPassword')

        # 验证新密码
        if not newPassword or len(newPassword) < 6:
            messages.error(request, '密码长度至少为6个字符！')
            return redirect('profile')

        if newPassword != confirmPassword:
            messages.error(request, '两次输入的密码不一致！')
            return redirect('profile')

        # 更新密码
        hashed_new_password = hashlib.md5(newPassword.encode()).hexdigest()
        userInfo.password = hashed_new_password
        userInfo.save()

        messages.success(request, '密码修改成功！')
        return redirect('profile')

    cites = getGlobalData()
    return render(request, 'profile.html', {
        'userInfo': userInfo,
        'cites': cites
    })




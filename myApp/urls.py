from django.contrib import admin
from django.urls import path, include
from myApp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('cityChar', views.cityChar, name='cityChar'),
    path('tableData', views.tableData, name='tableData'),
    path('api/map-data/', views.map_data_api, name='map_data_api'),
    path('wordCloud', views.wordCloud, name='wordCloud'),
    path('weatherForecast', views.weatherForecast, name='weatherForecast'),
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
]
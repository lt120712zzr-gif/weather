from django.contrib import admin
from django.urls import path, include
from myApp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('cityChar', views.cityChar, name='cityChar'),
    path('tableData', views.tableData, name='tableData'),
    path('api/map-data/', views.map_data_api, name='map_data_api'),
]
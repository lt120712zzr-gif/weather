from django.contrib import admin
from django.urls import path, include
from myApp import views

urlpatterns = [
    path('index',views.index,name='index'),
    path('cityChar',views.cityChar,name='cityChar'),
    path('tableData',views.tableData,name='tableData'),
]
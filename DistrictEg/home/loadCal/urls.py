from django.urls import path,include
from django.conf.urls import url
from . import views
from django.contrib import admin


urlpatterns = [
    path('',views.home,name='home'),
    # url( r'^loadCal/', views.loadCal, name='loadCal' ),
    url( r'^CalLoads/', views.CalLoads, name='CalLoads' ),
]

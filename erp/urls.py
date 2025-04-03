 
from django.contrib import admin
from django.urls import path,include 
from . import views
urlpatterns = [
     path('', views.dashboard, name='dashboard'),
     path('dispatch/mark-delivered/', views.dispatch_view, name='mark_dispatch_delivered'),
    
]

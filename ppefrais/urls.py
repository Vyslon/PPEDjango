from django.contrib import admin
from django.urls import path
from ppefrais import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('disconnect/', views.disconnect, name='disconnect')
]

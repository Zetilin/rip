from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('reactors/<int:reactor_id>/', reactor),
    path('stations/<int:station_id>/', station),
]
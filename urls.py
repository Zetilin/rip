from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('reactors/<int:reactor_id>/', reactor_details, name="reactor_details"),
    path('reactors/<int:reactor_id>/add_to_station/', add_reactor_to_draft_station, name="add_reactor_to_draft_station"),
    path('stations/<int:station_id>/delete/', delete_station, name="delete_station"),
    path('stations/<int:station_id>/', station)
]

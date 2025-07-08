from .views import *

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("server_status/", server_status),
    path("server_time/", server_time),
    path("server_configured/", server_configured),
    path("get_current_medicines/", get_current_medicines),
    
    # TODO: schedule
    path("taken/<int:medicine_id>", update_medicine_status),
]

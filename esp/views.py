import datetime

from django.shortcuts import render
from django.http import JsonResponse
# from .models import Medicine

# Create your views here.
def server_status(request):
    return JsonResponse({"status": "ok"})

def server_time(request):
    # damascus time
    dt = datetime.datetime.now()
    return JsonResponse({
        "year": dt.year,
        "day": dt.day, 
        "hour": dt.hour,
        "minute": dt.minute,
        "second": dt.second,
        "microsecond": dt.microsecond
        })

def schedule(request):
    return JsonResponse({"TODO": ""})

def update_medicine_status(request, medicine_id):
    return JsonReoinse({"TODO": ""})

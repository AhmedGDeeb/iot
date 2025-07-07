import datetime

from django.shortcuts import render
from django.http import JsonResponse
from .models import Medicine

# Create your views here.
def server_status(request):
    return JsonResponse({"status": "OK"})

def server_time(request):
    # damascus time
    dt = datetime.datetime.now()
    return JsonResponse({
        "year": dt.year,
        "day": dt.day,
        "month": dt.month,
        "hour": dt.hour,
        "minute": dt.minute,
        "second": dt.second,
        })

def schedule(request):
    Medicine.objects.all()
    return JsonResponse({"TODO": ""})

def update_medicine_status(request, medicine_id):
    return JsonResponse({"TODO": ""})

import datetime

from django.shortcuts import render
from django.http import JsonResponse
from .models import Medicine

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
    try:
        medicine = Medicine.objects.get(medicine_id=medicine_id)
        medicine.status = 'taken'
        medicine.save()
        return JsonResponse({
            'status': 'ok',
            'medicine_id': medicine_id,
        })
    except Medicine.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'medicine_id': medicine_id,
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'medicine_id': medicine_id,
        })
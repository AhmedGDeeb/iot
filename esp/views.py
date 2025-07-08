import datetime

from django.utils import timezone
from django.http import JsonResponse
from django.utils import timezone
from .models import deviceConfigurations, Medicine
from django.shortcuts import get_object_or_404

# Create your views here.
def server_status(request):
    return JsonResponse({"status": "OK"})

def server_time(request):
    dt = timezone.now()
    return JsonResponse({
        "year": dt.year,
        "day": dt.day,
        "month": dt.month,
        "hour": dt.hour,
        "minute": dt.minute,
        "second": dt.second,
        })

def server_configured(request):
    if len(deviceConfigurations.objects.all()) != 0:
        obj = deviceConfigurations.objects.get(pk=1)
        return JsonResponse({'status': 'NOT OK', 'slots_count': obj.slots_count})
    return JsonResponse({'status': 'OK'})

def get_current_medicines(request):
    now = timezone.now()
    
    # Query medicines with future dates and specified statuses
    medicines = Medicine.objects.filter(
        medicine_date__gt=now,
        medicine_date__lt=now+datetime.timedelta(minutes=1),
        status__in=['SCHEDULED', 'SENT']  # Only these statuses
    ).order_by('-medicine_date')
    
    # Prepare the response data
    medicine_data = []
    for med in medicines:
        medicine_data.append({
            'medicine_id': med.medicine_id,
            'medicine_name': med.medicine_name,
            'year': med.medicine_date.year,
            'day': med.medicine_date.day,
            'hour': med.medicine_date.hour,
            'minute': med.medicine_date.minute,
            'slot_number': med.slot_number,
            'status': med.status
        })
    
    # Return as JSON response
    return JsonResponse({'medicines': medicine_data}, safe=False)

def update_medicine_status(request, medicine_id):
    try:
        obj = get_object_or_404(Medicine, medicine_id=medicine_id)
        obj.status = 'TAKEN'
        obj.save()
    except Exception as e:
        print(e)
        return JsonResponse({"status": "NOT OK"})
    return JsonResponse({"status": "OK"})

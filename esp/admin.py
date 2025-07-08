from django.contrib import admin
from django.contrib.auth.models import User, Group

# Unregister the default User and Group models
admin.site.unregister(User)
admin.site.unregister(Group)

from .models import deviceConfigurations, Medicine
# Register your models here.
admin.site.register(deviceConfigurations)


class MedicineAdmin(admin.ModelAdmin):
    list_filter = ('medicine_name', 'medicine_date', 'slot_number', 'status')

admin.site.register(Medicine, MedicineAdmin)
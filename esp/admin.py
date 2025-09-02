from django.contrib import admin
from django.contrib.auth.models import User, Group

# Unregister the default User and Group models
admin.site.unregister(User)
admin.site.unregister(Group)

from .models import deviceConfigurations
# Register your models here.
admin.site.register(deviceConfigurations)

from .models import Medicine
from django import forms
class MedicineAdminForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        frequency = cleaned_data.get('frequency')
        frequency = cleaned_data.get('times_to_repeat')
        repeat_until = cleaned_data.get('repeat_until')
        
        if frequency != 'once' and not repeat_until:
            raise forms.ValidationError(
                "You must specify an end date for recurring events"
            )
        return cleaned_data
    
@admin.register(Medicine)
class EventAdmin(admin.ModelAdmin):
    form = MedicineAdminForm
    list_display = ('medicine_name', 'medicine_date', 'slot_number', 'frequency', 'is_recurring')
    list_filter = ('medicine_name', 'medicine_date', 'slot_number', 'status', 'frequency', 'is_recurring')
    fieldsets = (
        (None, {
            'fields': ('medicine_name', 'medicine_date', 'slot_number', 'status')
        }),
        ('Recurrence', {
            'fields': ('frequency', 'times_to_repeat', 'repeat_until'),
            'classes': ('collapse',)
        }),
    )
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj and obj.is_generated:
            # Hide recurrence options for generated events
            return (fieldsets[0],)
        return fieldsets
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.is_generated:
            return ['medicine_name', 'medicine_date', 'end_datetime', 'frequency', 'times_to_repeat', 'repeat_until']
        return super().get_readonly_fields(request, obj)
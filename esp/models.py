from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class deviceConfigurations(models.Model):
    """Model to store the maximum slot number available"""
    max_slots = models.PositiveIntegerField(
        default=4,
        validators=[MinValueValidator(1)],
        help_text="Maximum number of medication slots available in a day"
    )
    
    def save(self, *args, **kwargs):
        # Ensure there's only one instance of this model
        self.pk = 1
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Max Slots: {self.max_slots}"
    
    @classmethod
    def get_max_slots(cls):
        """Helper method to get the current max slots"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj.max_slots
    
class Medicine(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('sent', 'Sent'),
        ('taken', 'Taken'),
    ]
    
    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=100)
    medicine_date = models.DateTimeField(auto_now_add=True)
    slot_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(deviceConfigurations().get_max_slots())],
        help_text="Which slot this medicine belongs to (1, 2, 3, etc.)"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='scheduled'
    )
    
    def __str__(self):
        return f"Medicine {self.medicine_id} - {self.status}"

    class Meta:
        ordering = ['-medicine_date']
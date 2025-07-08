from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class deviceConfigurations(models.Model):
    @classmethod
    def get_num_slots(cls):
        """Helper method to get the current max slots"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj.slots_count
    
    slots_count = models.PositiveIntegerField(
        default=4,
        validators=[MinValueValidator(1)],
        help_text="number of medication slots"
    )
    def save(self, *args, **kwargs):
        # Ensure there's only one instance of this model
        self.pk = 1
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"#Slots: {self.slots_count}"

    
    
class Medicine(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', 'SCHEDULED'),
        ('SENT', 'SENT'),
        ('TAKEN', 'TAKEN'),
    ]

    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=100, blank=False, null=False)
    medicine_date = models.DateTimeField(blank=False, null=False)
    slot_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='SCHEDULED'
    )

    def __str__(self):
        return f"{self.medicine_name}@{self.medicine_id} - {self.medicine_date} - slot: {self.slot_number} - status: {self.status}"

    class Meta:
        ordering = ['-medicine_date']
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

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
    FREQUENCY_CHOICES = [
        ('once', 'once'),
        ('days', 'days'),
        ('weeks', 'weeks'),
        ('hours', 'hours'),
        ('minutes', 'minutes'),
    ]

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
    frequency = models.CharField(
        max_length=10, 
        choices=FREQUENCY_CHOICES, 
        default='once'
    )
    times_to_repeat = models.IntegerField(default='0', blank=False, null=False)
    repeat_until = models.DateTimeField(blank=True, null=True)
    is_recurring = models.BooleanField(default=False)

    def clean(self):
        if self.is_recurring and not self.repeat_until:
            raise ValidationError("Repeat until date is required for recurring events")
        if self.repeat_until and self.repeat_until < self.medicine_date:
            raise ValidationError("Repeat until date must be after start date")
    
    def save(self, *args, **kwargs):
        self.is_recurring = self.frequency != 'once'
        super().save(*args, **kwargs)
        if self.is_recurring:
            self.generate_recurring_events()

    def generate_recurring_events(self):
        from datetime import timedelta
        
        # Delete existing generated events for this series
        Medicine.objects.filter(
            original_event=self,
            is_generated=True
        ).delete()
        
        if not self.is_recurring:
            return
            
        current = self.medicine_date
        delta = None
        
        if self.frequency == 'days':
            delta = timedelta(days=1) * self.times_to_repeat
        elif self.frequency == 'weeks':
            delta = timedelta(weeks=1) * self.times_to_repeat
        elif self.frequency == 'hours':
            delta = timedelta(hours=1) * self.times_to_repeat
        elif self.frequency == 'minutes':
            delta = timedelta(minutes=1) * self.times_to_repeat
        
        while current <= self.repeat_until:
            if current != self.medicine_date:  # Don't recreate the original
                Medicine.objects.create(
                    medicine_name=self.medicine_name,
                    medicine_date=current,
                    slot_number=self.slot_number,
                    original_event=self,
                    is_generated=True,
                    frequency='once'  # Generated events shouldn't recur
                )
            current += delta
    
    original_event = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='generated_events'
    )
    is_generated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.medicine_name}@{self.medicine_id} - {self.medicine_date} - slot: {self.slot_number} - status: {self.status} - frequency: {self.frequency}"

    class Meta:
        ordering = ['-medicine_date']
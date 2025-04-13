from django.db import models
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_length=200)
    banner = models.ImageField(upload_to='event_banners/')
    participants = models.PositiveIntegerField()  # Maximum participants
    current_participants = models.PositiveIntegerField(default=0) # Current number of participants
    date = models.DateTimeField()  # Changed from DateField to DateTimeField
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2)
    prize_pool = models.DecimalField(max_digits=10, decimal_places=2)
    joined_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participated_events', blank=True)

    def __str__(self):
        return self.title

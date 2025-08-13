from django.db import models
from django.contrib.auth import get_user_model

Account = get_user_model()


class Event(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Account, related_name='user_events',
                                   on_delete=models.CASCADE)


class UserEvent(models.Model):
    calendar = models.ForeignKey(Account, related_name='calendar_events',
                                 on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

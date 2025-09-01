from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SocialProfile(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=20, null=False, blank=False,
                                    default='Change Me')
    # TODO: Add profile image support
    description = models.CharField(max_length=120, blank=True)
    is_bot = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.display_name} at {self.created_at.date()}'

from mitaba import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

DEFAULT_OWNER_ID = 1


class User(AbstractUser):
    def get_profile(self):
        try:
            profile = Profile.objects.get(owner=self)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(owner=self)
        return profile


class Profile(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 default=DEFAULT_OWNER_ID)
    picture_url = models.URLField(blank=True)

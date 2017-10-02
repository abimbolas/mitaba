import uuid
from mitaba import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

DEFAULT_OWNER_ID = 1


class User(AbstractUser):
    pass
    # object_uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)


class Profile(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='profile',
                              on_delete=models.CASCADE,
                              default=DEFAULT_OWNER_ID)
    picture_url = models.URLField()

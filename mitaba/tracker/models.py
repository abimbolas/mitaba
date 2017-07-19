from django.db import models
from django.contrib.postgres.fields import ArrayField

DEFAULT_OWNER_ID = 1


class Entry(models.Model):
    owner = models.ForeignKey('auth.User', related_name='entry', on_delete=models.CASCADE, default=DEFAULT_OWNER_ID)
    start = models.DateTimeField()
    stop = models.DateTimeField()
    details = ArrayField(
        models.CharField(max_length=500, blank=False),
        blank=False,
        max_length=20,
        db_index=True
    )

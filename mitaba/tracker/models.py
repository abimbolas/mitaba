from django.db import models
from django.contrib.postgres.fields import ArrayField


class Entry(models.Model):
    start = models.DateTimeField()
    stop = models.DateTimeField()
    details = ArrayField(
        models.CharField(max_length=500, blank=False),
        blank=False,
        max_length=20
    )

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class Entry(models.Model):
  user = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
  start = models.DateTimeField()
  stop = models.DateTimeField()
  details = ArrayField(models.CharField(max_length=500), size=20)

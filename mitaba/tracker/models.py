from django.db import models
# from django.contrib.postgres.fields import ArrayField


class Entry(models.Model):
    start = models.DateTimeField()
    stop = models.DateTimeField()
    # details = ArrayField() todo: convert to ArrayField lately
    details = models.TextField()

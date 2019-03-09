from django.db import models

from core.utils import generate_key


class Dscan(models.Model):
    key = models.CharField(max_length=8, unique=True, default=generate_key)
    system = models.ForeignKey('sde.System', null=True, default=None, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class DscanObject(models.Model):
    scan = models.ForeignKey(Dscan, related_name="dscan_objects", on_delete=models.CASCADE)
    type = models.ForeignKey('sde.Type', related_name="dscan_objects", on_delete=models.CASCADE)
    name = models.TextField()
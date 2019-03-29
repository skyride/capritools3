from django.contrib.auth.models import User
from django.db import models

from core.utils import generate_key


class Localscan(models.Model):
    key = models.CharField(max_length=80, unique=True, default=generate_key)
    user = models.ForeignKey(User, related_name="localscans", null=True, default=None, on_delete=models.CASCADE)
    raw = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class LocalscanItem(models.Model):
    scan = models.ForeignKey(Localscan, related_name="items", on_delete=models.CASCADE)
    raw = models.TextField()

    character = models.ForeignKey('core.Character', related_name="localscan_items", on_delete=models.CASCADE)
    corporation = models.ForeignKey('core.Corporation', related_name="localscan_items", on_delete=models.CASCADE)
    alliance = models.ForeignKey('core.Alliance', related_name="localscan_items", on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
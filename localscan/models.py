from django.contrib.auth.models import User
from django.db import models

from core.utils import generate_key
from core.models import Alliance, Corporation, Character
from sde.models import Faction


class Localscan(models.Model):
    key = models.CharField(max_length=80, unique=True, default=generate_key)
    user = models.ForeignKey(User, related_name="localscans", null=True, default=None, on_delete=models.CASCADE)
    raw = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class LocalscanItem(models.Model):
    scan = models.ForeignKey(Localscan, related_name="items", on_delete=models.CASCADE)

    character = models.ForeignKey(Character, related_name="localscan_items", on_delete=models.CASCADE)
    corporation = models.ForeignKey(Corporation, related_name="localscan_items", on_delete=models.CASCADE)
    alliance = models.ForeignKey(Alliance, null=True, default=None, related_name="localscan_items", on_delete=models.CASCADE)
    faction = models.ForeignKey(Faction, null=True, default=None, related_name="localscan_items", on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
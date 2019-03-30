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


class Coalition(models.Model):
    scan = models.ForeignKey(Localscan, related_name="coalitions", on_delete=models.CASCADE)

    _id = models.CharField(max_length=32, db_index=True)
    name = models.CharField(max_length=128, db_index=True)
    colour = models.CharField(max_length=7)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class LocalscanItem(models.Model):
    scan = models.ForeignKey(Localscan, related_name="items", on_delete=models.CASCADE)

    character = models.ForeignKey(Character, related_name="localscan_items", on_delete=models.CASCADE)
    corporation = models.ForeignKey(Corporation, related_name="localscan_items", on_delete=models.CASCADE)
    alliance = models.ForeignKey(Alliance, null=True, default=None, related_name="localscan_items", on_delete=models.CASCADE)
    faction = models.ForeignKey(Faction, null=True, default=None, related_name="localscan_items", on_delete=models.CASCADE)
    coalition = models.ForeignKey(Coalition, null=True, default=None, related_name="items", on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
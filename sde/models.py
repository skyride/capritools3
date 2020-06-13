# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from math import pow, sqrt

from django.db import models


# Map
class Region(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    radius = models.FloatField(null=True)

    def __str__(self):
        return "%s:%s" % (self.id, self.name)


class Constellation(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    region = models.ForeignKey(Region, related_name="constellations", on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    radius = models.FloatField(null=True)

    def __str__(self):
        return "%s:%s" % (self.id, self.name)


class System(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    region = models.ForeignKey(Region, related_name="systems", on_delete=models.CASCADE)
    constellation = models.ForeignKey(Constellation, related_name="systems", on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    luminosity = models.FloatField()
    border = models.BooleanField()
    fringe = models.BooleanField()
    corridor = models.BooleanField()
    hub = models.BooleanField()
    international = models.BooleanField()
    security = models.FloatField()
    radius = models.FloatField(null=True)
    sun = models.ForeignKey('Type', null=True, default=None, on_delete=models.CASCADE)
    security_class = models.CharField(max_length=2, null=True)

    def __str__(self):
        return self.name


    # Compares distance between self and a target system
    def distance(self, target, ly=False):
        x = pow(target.x - self.x, 2)
        y = pow(target.y - self.y, 2)
        z = pow(target.z - self.z, 2)

        distance = sqrt(x + y + z)
        if ly:
            return distance / 9460730472580800
        else:
            return distance


class SystemJump(models.Model):
    origin = models.ForeignKey(System, related_name="jumps_origin", on_delete=models.CASCADE)
    destination = models.ForeignKey(System, related_name="jumps_destination", on_delete=models.CASCADE)

    def __str__(self):
        return "%s -> %s" % (self.origin.name, self.destination.name)


# NPC Entities
class Faction(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=128, db_index=True)
    description = models.TextField()
    system = models.ForeignKey(System, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def image128(self):
        return f"https://imageserver.eveonline.com/Alliance/{self.id}_128.png"


# Types
class MarketGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    parent = models.ForeignKey('self', null=True, default=None, db_constraint=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    icon_id = models.IntegerField(null=True)
    has_types = models.BooleanField()

    def __str__(self):
        return "%s:%s" % (self.id, self.name)


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    icon_id = models.IntegerField(null=True)
    published = models.BooleanField()

    def __str__(self):
        return "%s:%s" % (self.id, self.name)


class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    category = models.ForeignKey(Category, related_name="groups", on_delete=models.CASCADE)
    icon_id = models.IntegerField(null=True)
    anchored = models.BooleanField(null=True)
    anchorable = models.BooleanField(null=True)
    fittable_non_singleton = models.BooleanField(null=True)
    published = models.BooleanField()

    def __str__(self):
        return "%s:%s" % (self.id, self.name)


class Type(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(Group, related_name="types", null=True, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=True)
    mass = models.FloatField(null=True)
    volume = models.FloatField(null=True)
    capacity = models.FloatField(null=True)
    published = models.BooleanField()
    market_group = models.ForeignKey(MarketGroup, null=True, on_delete=models.CASCADE)
    icon_id = models.IntegerField(null=True)

    buy = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    sell = models.DecimalField(max_digits=16, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    def image32(self):
        return self._image_url(32)

    def image64(self):
        return self._image_url(64)

    def _image_url(self, size):
        return f"https://imageserver.eveonline.com/Render/{self.id}_{size}.png"


class AttributeCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=200, null=True)

    def __str__(self):
        return "%s:%s" % (self.id, self.name)


class AttributeType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=400, null=True)
    category = models.ForeignKey(AttributeCategory, null=True, db_constraint=False, related_name="types", on_delete=models.CASCADE)

    description = models.CharField(max_length=1000, null=True)
    icon_id = models.IntegerField(null=True)
    default_value = models.IntegerField(null=True)
    published = models.BooleanField(db_index=True)
    display_name = models.CharField(max_length=150, null=True)
    unit_id = models.IntegerField(null=True)
    stackable = models.BooleanField()
    high_is_good = models.BooleanField()

    def __str__(self):
        return "%s:%s" % (self.id, self.name)


class TypeAttribute(models.Model):
    type = models.ForeignKey(Type, related_name="attributes", on_delete=models.CASCADE)
    attribute = models.ForeignKey(AttributeType, related_name="types", on_delete=models.CASCADE)
    value_int = models.IntegerField(null=True)
    value_float = models.FloatField(null=True)

    @property
    def value(self):
        if self.value_int != None:
            return self.value_int
        else:
            return self.value_float

    def __str__(self):
        return "%s (%s)" % (
            self.attribute.name,
            self.value
        )


class Station(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    type = models.ForeignKey(Type, null=True, default=None, on_delete=models.CASCADE)
    system = models.ForeignKey(System, null=True, default=None, on_delete=models.CASCADE)
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    z = models.FloatField(default=0)

    # Is the station a structure or an NPC station
    structure = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return "%s:%s" % (self.id, self.name)


# Maps denormalised
class MapItem(models.Model):
    type = models.ForeignKey(Type, null=True, related_name="map_items", on_delete=models.SET_NULL)
    system = models.ForeignKey(System, null=True, related_name="map_items", on_delete=models.CASCADE)

    name = models.CharField(max_length=100, null=True, db_index=True)

    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    z = models.FloatField(default=0)

from django.db import models


class Alliance(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=128, db_index=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def image128(self):
        return f"https://imageserver.eveonline.com/Alliance/{self.id}_128.png"


class Corporation(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=128, db_index=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def image64(self):
        return f"https://imageserver.eveonline.com/Corporation/{self.id}_64.png"


class Character(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=128, db_index=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
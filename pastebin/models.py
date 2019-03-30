import bcrypt

from django.contrib.auth.models import User
from django.db import models

from core.utils import generate_key


class Paste(models.Model):
    key = models.CharField(max_length=80, unique=True, default=generate_key)
    user = models.ForeignKey(User, related_name="pastes", null=True, default=None, on_delete=models.CASCADE)

    text = models.TextField()
    password = models.CharField(max_length=128, null=True, default=None, blank=True)
    expires = models.DateTimeField(null=True, default=None, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def check_password(self, password):
        """Check if the password provided matches the model"""
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
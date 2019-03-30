import bcrypt

from datetime import timedelta

from django import forms
from django.utils.timezone import now

from .models import Paste


class PasteForm(forms.ModelForm):
    EXPIRES_CHOICES = [
        (0, "Never"),
        (3, "3 hours"),
        (6, "6 hours"),
        (24, "1 day"),
        (72, "3 days"),
        (720, "30 days")
    ]

    expires = forms.ChoiceField(choices=EXPIRES_CHOICES)

    class Meta:
        model = Paste
        fields = (
            'text',
            'password',
            'expires'
        )

    def clean_expires(self):
        """Returns a datetime with the number of hours added to it"""
        hours = int(self.cleaned_data['expires'])
        if hours == 0:
            return None
        return now() + timedelta(hours=hours)

    def clean_password(self):
        password = self.cleaned_data['password']
        if password:
            return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, paste=None, **kwargs):
        self.paste = paste
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.paste.check_password(password):
            raise forms.ValidationError("Incorrect Password")
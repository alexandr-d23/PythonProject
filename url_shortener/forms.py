import re

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from url_shortener.models import User, UrlWithShortcut


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class UrlForm(forms.ModelForm):
    full_url = forms.URLField(widget=forms.URLInput(
        attrs={"placeholder": "URL", "class": "input"}
    ))

    class Meta:
        model = UrlWithShortcut
        fields = ('full_url',)
        exclude = ['user',]

from django.contrib.auth.forms import UserCreationForm
from django import forms

from url_shortener.models import User, UrlWithShortcut


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class UrlForm(forms.ModelForm):
    url = forms.URLField(widget=forms.URLInput(
        attrs={"placeholder": "URL"}
    ))

    class Meta:
        model = UrlWithShortcut
        fields = ('url',)
        exclude = ['user']

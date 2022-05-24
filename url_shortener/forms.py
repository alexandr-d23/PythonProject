from django.contrib.auth.forms import UserCreationForm

from url_shortener.models import User


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

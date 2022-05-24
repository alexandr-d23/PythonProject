from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models import CASCADE


class User(AbstractUser):
    pass


class UrlWithShortcut(models.Model):
    usage_count = models.PositiveIntegerField(default=0)
    full_url = models.URLField
    url_shortcut = models.CharField
    user = models.ForeignKey(User, on_delete=CASCADE)


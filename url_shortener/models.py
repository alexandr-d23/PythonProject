from random import choice
from string import ascii_letters, digits
import bcrypt

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models import CASCADE


class User(AbstractUser):
    pass


class UrlWithShortcut(models.Model):
    usage_count = models.PositiveIntegerField(default=0)
    full_url = models.URLField(default='')
    url_shortcut = models.CharField(max_length=12)
    user = models.ForeignKey(User, on_delete=CASCADE)

    def save(self, *args, **kwargs):
        while not self.url_shortcut or self.__class__.objects.filter(url_shortcut=self.url_shortcut).exclude(
                full_url=self.full_url).exists():
            self.url_shortcut = get_short_url()
        super().save(*args, **kwargs)


def get_short_url(url):
    salt = bcrypt.gensalt()
    hashedUrl = bcrypt.hashpw(url.encode('utf-8'), salt).decode()
    print(hashedUrl)
    return hashedUrl[0:6]

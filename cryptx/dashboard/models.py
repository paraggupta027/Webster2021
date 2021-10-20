from django.db import models

from django.contrib.auth import get_user_model
from coins.models import Coin

User=get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    email = models.CharField(max_length=50 , default="")

    def __str__(self):
        return self.email



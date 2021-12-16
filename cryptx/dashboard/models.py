from django.db import models

from django.contrib.auth import get_user_model
from django.db.models.fields import NullBooleanField
from coins.models import Coin

User=get_user_model()

class Profile(models.Model):
#     user = models.ForeignKey(User , on_delete = models.CASCADE)
    email = models.CharField(max_length=50 , default="")
    money = models.IntegerField(default=0)

    @classmethod
    def get_money(cls,email):
        return Profile.objects.get(email=email).money

    def __str__(self):
        return self.email



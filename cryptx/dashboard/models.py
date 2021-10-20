from django.db import models

from django.contrib.auth import get_user_model
from django.db.models.fields import NullBooleanField
from coins.models import Coin

User=get_user_model()

class Profile(models.Model):
    email = models.CharField(max_length=50,default="")
    # user = models.OneToOneField(User,on_delete = models.CASCADE,null=True)

    def __str__(self):
       return self.email





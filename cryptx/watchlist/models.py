from django.db import models

from django.contrib.auth import get_user_model
from coins.models import Coin

User=get_user_model()
# Create your models here.


class WatchList(models.Model):
    name = models.CharField(max_length=50,default="")
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    coins = models.ManyToManyField(Coin,related_name='coins',blank=True)

    def __str__(self):
       return self.user.first_name + " " + self.name


# watchlist boht sari-----har wl k boht sare coins
# wl foreign user
# particular wl usme diff coins

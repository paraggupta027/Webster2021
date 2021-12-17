from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.db.models.query_utils import Q
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.db.models.fields import NullBooleanField
from coins.models import Coin
from dashboard.models import Profile
User=get_user_model()
# Create your models here.
class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    coin = models.ForeignKey(Coin, on_delete=CASCADE)
    quantity = models.FloatField(default=0)
    avg_price = models.FloatField(default=0)

    @classmethod
    def get_quantity(cls,user,coin):
        obj, create = cls.objects.get_or_create(user=user,coin=coin)
        return obj.quantity

    @classmethod 
    def buy_coin(cls,user,quantity,price,coin):
        obj, create = cls.objects.get_or_create(user=user,coin=coin)
        total_prev_price = obj.quantity * obj.avg_price
        total_quantity = obj.quantity + quantity
        total_new_price = price*quantity + total_prev_price
        new_avg_price = total_new_price/total_quantity
        obj.quantity = total_quantity
        obj.price = new_avg_price
        obj.save()

    @classmethod
    def sell_coin(cls,user,quantity,price,coin):
        obj, create = cls.objects.get(user=user,coin=coin)
        total_quantity = obj.quantity - quantity
        obj.quantity = total_quantity
        obj.save()

    def __str__(self):
        return f'{self.user.email} {self.coin.name}'
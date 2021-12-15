from django.db import models

from django.contrib.auth import get_user_model
from django.db.models.fields import NullBooleanField
from coins.models import Coin
from dashboard.models import Profile

from orders.coin_price_api import get_coin_price

User=get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    quantity = models.FloatField()
    coin = models.ForeignKey(Coin,on_delete=models.CASCADE)
    # status = models.

    @classmethod
    def can_be_executed(cls,user,coin_symbol,quantity):
        cur_user = Profile.objects.get(email=user.email)
        cur_coin_price = get_coin_price(coin_symbol)

        user_money = cur_user.money
        print(cur_coin_price*quantity)

        if cur_coin_price*quantity>user_money:
            print("Not Enough Balance")
            return False
        
        # Save new order in DB
        coin_obj = Coin.objects.get(symbol=coin_symbol)

        new_order = Order(user=user,quantity=quantity,coin=coin_obj)
        new_order.save()
        return True


    def __str__(self):
        return self.user.email + " , order id: " + str(self.id)



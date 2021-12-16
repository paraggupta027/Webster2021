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
    def can_be_executed(cls,user,coin_symbol,quantity,mode):
        cur_user = Profile.objects.get(email=user.email)
        cur_coin_price = get_coin_price(coin_symbol)
        if mode is  "BUY":
            user_money = cur_user.money
            print(cur_coin_price*quantity)

            if cur_coin_price*quantity>user_money:
                print("Not Enough Balance")
                return False ,"Not Enough Balance , only sufficient for "+str(round(user_money/cur_coin_price,5)) + " "+ coin_symbol
        if mode is "SELL":
            coin_quantity = cls.get_quantity(user=user,coin_symbol=coin_symbol)
            if coin_quantity < quantity:
                print(f"Not Enough {coin_quantity}")
                return False ,f'Not enough {coin_symbol} only {coin_quantity} are available.'
        # Save new order in DB
        coin_obj = Coin.objects.get(symbol=coin_symbol)

        new_order = Order(user=user,quantity=quantity,coin=coin_obj)
        new_order.save()
        return True
    @classmethod
    def get_quantity(cls,user,coin_symbol):
    #TODO: get real quantity of coin w.r.t user from database
        return 2.1

    def _str_(self):
        return self.user.email + " , order id: " + str(self.id)
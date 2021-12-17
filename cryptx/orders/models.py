from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.db.models.fields import NullBooleanField
from coins.models import Coin
from dashboard.models import Profile
from portfolio.models import Portfolio
from orders.coin_price_api import get_coin_price

User=get_user_model()


class Order(models.Model):

    BUY,SELL = 1,2
    MODES = (
        (BUY, "Buy"),
        (SELL, "Sell"),
    )

    user = models.ForeignKey(User , on_delete = models.CASCADE)
    quantity = models.FloatField(default=0)
    coin = models.ForeignKey(Coin,on_delete=models.CASCADE)
    order_price = models.FloatField(default=0)
    time = models.DateTimeField(default=timezone.now)
    mode = models.PositiveSmallIntegerField(verbose_name="Mode", choices=MODES,default=1)


    class Meta:
        ordering=['-time']

    @classmethod
    def can_be_executed(cls,user,coin_symbol,quantity,mode):
        cur_user = Profile.objects.get(email=user.email)
        cur_coin_price = get_coin_price(coin_symbol)
        coin_obj = Coin.objects.get(symbol=coin_symbol)
        total_price = cur_coin_price*quantity
        print(total_price)

        if mode is cls.BUY:
            user_money = cur_user.money

            if cur_coin_price*quantity>user_money:
                print("Not Enough Balance")
                return False ,"Not Enough Balance , only sufficient for "+str(round(user_money/cur_coin_price,5)) + " "+ coin_symbol
            else:
                cur_user.money-=total_price
                cur_user.save()

        if mode is cls.SELL:
            coin_quantity = Portfolio.get_quantity(user=user,coin=coin_obj)
            if coin_quantity < quantity: 
                print(f"Not Enough {coin_quantity}")
                return False ,f'Not enough {coin_symbol} only {coin_quantity} are available.'
            else:
                cur_user.money+=total_price
                cur_user.save()


        # Save new order in DB
        

        new_order = Order(user=user,quantity=quantity,coin=coin_obj,order_price=cur_coin_price,mode=mode)
        new_order.save()
        return True
        
    def _str_(self):
        return self.user.email + " , order id: " + str(self.id)
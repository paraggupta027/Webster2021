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

    MARKET,LIMIT,STOPMARKET,STOPLIMIT = 1,2,3,4
    TYPES = (
        (MARKET,'MARKET'),
        (LIMIT,'LIMIT'),
        (STOPMARKET,'STOPMARKET'),
        (STOPLIMIT,'STOPLIMIT'),

    )
    
    PENDING,EXECUTED,CANCELLED,RUNNING = 1,2,3,4
    STATUS = (
        (PENDING,'PENDING'),
        (EXECUTED,'EXECUTED'),
        (CANCELLED,'CANCELLED'),
        (RUNNING,'RUNNING')
    )

    user = models.ForeignKey(User , on_delete = models.CASCADE)
    quantity = models.FloatField(default=0)
    coin = models.ForeignKey(Coin,on_delete=models.CASCADE)
    order_price = models.FloatField(default=0)
    order_type = models.PositiveSmallIntegerField(verbose_name="Type",choices=TYPES,default=1)
    order_status = models.PositiveSmallIntegerField(verbose_name="Status",choices=STATUS,default=1)
    time = models.DateTimeField(default=timezone.now)
    mode = models.PositiveSmallIntegerField(verbose_name="Mode", choices=MODES,default=1)


    class Meta:
        ordering=['-time']

    @classmethod
    def can_be_executed(cls,order_obj):
        # return True
        user=order_obj['user']
        coin_symbol = order_obj['coin_symbol']
        quantity = order_obj['quantity']
        mode = order_obj['mode']
        order_type = order_obj['order_type']
        limit_price = order_obj['limit_price']

        cur_user = Profile.objects.get(email=user.email)
        cur_coin_price = get_coin_price(coin_symbol)
        coin_obj = Coin.objects.get(symbol=coin_symbol)
        total_price = cur_coin_price*quantity

        print("Money Required: "+str(total_price))


        order_status=cls.EXECUTED
        if order_type==cls.LIMIT:
            order_status = cls.PENDING

        if mode is cls.BUY:
            user_money = cur_user.money

            if total_price>user_money:
                print("Not Enough Balance")
                return False ,"Not Enough Balance , only sufficient for "+str(round(user_money/cur_coin_price,5)) + " "+ coin_symbol
            else:
                if order_type==cls.MARKET:
                    # Add coin to portfolio
                    Portfolio.buy_coin(user,quantity,cur_coin_price,coin_obj)
                    cur_user.money-=total_price
                    cur_user.save()

                    # Save new order in DB
                    new_order = Order(
                        user=user,quantity=quantity,coin=coin_obj,
                        order_price=cur_coin_price,mode=mode,
                        order_status = cls.EXECUTED,
                        order_type = cls.MARKET
                    )
                    new_order.save()

                elif order_type==cls.LIMIT:
                     # Save new order in DB
                    new_order = Order(
                        user=user,quantity=quantity,coin=coin_obj,
                        order_price=limit_price,mode=mode,
                        order_status = cls.PENDING,
                        order_type = cls.LIMIT
                    )
                    new_order.save()
                    


        # if mode is cls.SELL:
        #     coin_quantity = Portfolio.get_quantity(user=user,coin=coin_obj)
        #     if coin_quantity < quantity: 
        #         print(f"Not Enough {coin_quantity}")
        #         return False ,f'Not enough {coin_symbol} only {coin_quantity} are available.'
        #     else:
        #         Portfolio.sell_coin(user,quantity,cur_coin_price,coin_obj)
        #         cur_user.money+=total_price
        #         cur_user.save()

        return True,new_order.id
        
    def __str__(self):
        return f'{self.user.email} , order id: {self.id} , coin: {self.coin.name}'

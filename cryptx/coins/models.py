from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model

User=get_user_model()

class Coin(models.Model):
    name = models.CharField(unique=True,max_length=30,default="")
    symbol = models.CharField(max_length=30,default="")

    def __str__(self):
       return f"{self.name}({self.symbol})"
    class Meta:
        verbose_name_plural = "Coin"
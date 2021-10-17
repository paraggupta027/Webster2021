from django.db import models

# Create your models here.

class Coin(models.Model):
    name = models.CharField(unique=True,max_length=30,default="")
    symbol = models.CharField(max_length=30,default="")

    def __str__(self):
       return self.name + " " + self.symbol

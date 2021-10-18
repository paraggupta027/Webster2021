from django.db import models

# Create your models here.

class Coin(models.Model):
    name = models.CharField(unique=True,max_length=30,default="")
    symbol = models.CharField(max_length=30,default="")
    # real_time_url = models.URLField(verbose_name="REAL TIME URL",blank=True)

    def __str__(self):
       return f"{self.name}({self.symbol})"
    class Meta:
        verbose_name_plural = "Coin"
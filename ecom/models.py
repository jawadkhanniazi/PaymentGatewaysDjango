from django.db import models

# Create your models here.

class Order(models.Model):
    pass

class ProductDeatils(models.Model):
    ids= models.IntegerField()   
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    details = models.CharField(max_length=10000, blank=True,null=True)
    
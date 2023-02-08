from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    file = models.FileField(upload_to="product_files/", blank=True,null=True)
    url = models.URLField()


    def __str__(self):
        return self.name
def get_display_price(self):
    return "{0:2f}".format(self.price / 100)


class OrderDetails(models.Model):
    product_id = models.IntegerField()
    customer_email = models.CharField(max_length=100)
    payment_method_type = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)
    order_status = models.CharField(max_length=100)
    jsonResonse = models.TextField()

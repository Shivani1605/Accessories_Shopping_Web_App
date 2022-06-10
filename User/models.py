from django.db import models
from Admin.models import Product

# Create your models here.  #while user getting signup data will be stored in ****UserInfo**** table
class UserInfo(models.Model):
    
    username = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=20)


    class Meta:
        db_table = "UserInfo"   #name of table if we not add this class name take automatic samething

class MyCart(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)     #it has username and password
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)    # it has all product in database so user add only thoes product add which are in database
    qty = models.IntegerField()

    
    class Meta:
        db_table = "MyCart"
    


class Payment(models.Model):
    uname = models.CharField(max_length=20)
    card_no = models.CharField(max_length=16)
    cvv = models.CharField(max_length=4)
    expiry = models.CharField(max_length=8)
    balance = models.FloatField(default=10000)

    class Meta:
        db_table = "Payment"   


class Order_Master(models.Model):
    username = models.CharField(max_length=20)
    date_Of_Oreder = models.DateField()
    amount = models.FloatField(default=100)
    product_details = models.CharField(max_length=100)

    class Meta:
        db_table = "Order_Master"

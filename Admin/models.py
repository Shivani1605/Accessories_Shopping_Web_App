from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = "Category"

class Product(models.Model):
    product_name = models.CharField(max_length=20)
    price = models.FloatField(default=200)
    imgurl = models.ImageField(upload_to="images")
    cat_id = models.ForeignKey(Category,on_delete=models.CASCADE)
     
    def __str__(self):
        return self.product_name

    class Meta:
        db_table = "Product"



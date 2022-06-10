from django.contrib import admin
from Admin.models import Category, Product
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','category_name')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','product_name','price','imgurl','cat_id')



admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
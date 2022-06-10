from django.contrib import admin
from User.models import Payment

# Register your models here.


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id','uname','card_no','cvv','expiry','balance')
    


admin.site.register(Payment,PaymentAdmin)

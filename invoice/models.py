from django.db import models
from django.db.models import F,Sum


# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    created_at = models.DateField()

    def __str__(self):
        return self.username
    from django.db.models import Sum, F


    @property
    def total_amount(self):
        total = Item.objects.filter(customer_name=self).aggregate(
            total=Sum(F('quantity') * F('price'))
        )['total'] 
        return total or 0 

    @property
    def total_paid_amount(self):
        total_paid = Item.objects.filter(customer_name=self).aggregate(
            total=Sum(F('paid_amount'))
        )['total']
        return total_paid or 0 

    @property
    def remaining_amount(self):
        return self.total_amount - self.total_paid_amount

    
    
class Item(models.Model):
    medicine = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.IntegerField()
    paid_amount = models.IntegerField(default=0)
    customer_name=models.ForeignKey(UserInfo, on_delete=models.CASCADE,null=True)
    
 
    @property
    def amount(self):
        return self.quantity * self.price

 
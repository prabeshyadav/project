from django import forms

from .models import UserInfo,Item

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['username', 'father_name','grand_parent', 'address', 'phone', 'created_at','minor','registered']




class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['medicine', 'quantity', 'price','paid_amount']
        exclude = ['customer_name']

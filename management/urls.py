from django.contrib import admin
from django.urls import path
from invoice import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.customer_data, name='invoice'),
    path('newdata', views.home, name='home'),
    path('user_data/', views.user_data, name='user_data'),
    path('item/<int:customer_id>/', views.invoice, name='item'),  # Correct URL name here  
    path('delete/<int:id>/', views.delete_customer, name='delete_customer'),

]

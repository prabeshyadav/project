from django.contrib import admin
from django.urls import path
from invoice import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.customer_data, name='invoice'),  # Main customer data view
    path('newdata', views.home, name='home'),  # Form to add new customer data
    path('login/',views.custom_login,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('item/<int:customer_id>/', views.invoice, name='item'),  # User's items page
    path('delete/<int:id>/', views.delete_customer, name='delete_customer'),  # Delete customer URL
    path('user_profile', views.user_profile, name='user_profile'),  # View all users
    path('user_data/<int:id>/', views.user_data, name='user_data'),
]

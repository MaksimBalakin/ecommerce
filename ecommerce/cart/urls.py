from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:good_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:good_id>/', views.cart_remove, name='cart_remove'),
    path('', views.cart_detail, name='cart_detail'),
]
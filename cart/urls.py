from django.urls import path
from . import views


app_name = 'cart'


urlpatterns = [
    path('',
         views.cart_detail,
         name='cart_detail'),
    path('add/<int:dish_id>/',
         views.cart_add,
         name='cart_add'),
    path('remove/<int:dish_id>/',
         views.cart_remove,
         name='cart_remove'),
    path('add_random_food/',
         views.cart_add_random_food,
         name='cart_add_random_food'),
    path('add_random_drink/',
         views.cart_add_random_drink,
         name='cart_add_random_drink'),
]

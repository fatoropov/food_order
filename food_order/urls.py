from django.urls import path
from . import views


app_name = 'food_order'

urlpatterns = [
    path('',
         views.index,
         name='index'),
    path('dishes',
         views.dish_list,
         name='dish_list'),
    path('<slug:category_slug>/',
         views.dish_list,
         name='dish_list_by_category'),
    path('<int:id>/<slug:slug>/',
         views.dish_detail,
         name='dish_detail'),
]

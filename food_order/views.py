from django.shortcuts import render, get_object_or_404
from .models import Category, Dish
from cart.forms import CartAddDishForm


def index(request):
    """Домашняя страница сервиса"""
    return render(request, 'food_order/index.html')


def dish_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    dishes = Dish.objects.filter(available=True)
    cart_dish_form = CartAddDishForm()
    if category_slug:
        category = get_object_or_404(Category,
                                     slug=category_slug)
        dishes = dishes.filter(category=category)
    return render(request,
                  'food_order/dish/list.html',
                  {'category': category,
                   'categories': categories,
                   'dishes': dishes,
                   'cart_dish_form': cart_dish_form})


def dish_detail(request, id, slug):
    dish = get_object_or_404(Dish,
                             id=id,
                             slug=slug,
                             available=True)
    cart_dish_form = CartAddDishForm()
    return render(request,
                  'food_order/dish/detail.html',
                  {'dish': dish,
                   'cart_dish_form': cart_dish_form})

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from food_order.models import Dish
from .cart import Cart
from .forms import CartAddDishForm, CartUpdateQuantityDish
from django.contrib import messages

from random import choice


@require_POST
def cart_add(request, dish_id):
    cart = Cart(request)
    dish = get_object_or_404(Dish, id=dish_id)
    form = CartAddDishForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        quantity = cd['quantity']
        messages.success(request, f'Товар - "{dish}" ({quantity} шт.) добавлен в корзину')
        cart.add(dish=dish,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    else:
        messages.error(request, f'Ошибка \n Товар - {dish} не добавлен')
    return redirect('food_order:dish_list')


@require_POST
def cart_remove(request, dish_id):
    cart = Cart(request)
    dish = get_object_or_404(Dish, id=dish_id)
    cart.remove(dish)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request,
                  'cart/detail.html',
                  {'cart': cart})


def cart_update_plus(request, dish_id):
    cart = Cart(request)
    dish = get_object_or_404(Dish, id=dish_id)
    form = CartUpdateQuantityDish(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(dish=dish,
                 quantity=1,
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')


def cart_update_minus(request, dish_id):
    cart = Cart(request)
    dish = get_object_or_404(Dish, id=dish_id)
    form = CartUpdateQuantityDish(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.remove(dish=dish,
                    quantity=1,
                    override_quantity=cd['override'])
    return redirect('cart:cart_detail')


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')


@require_POST
def cart_add_random_food(request):
    cart = Cart(request)
    eda = [dish for dish in list(Dish.objects.all().values())
           if dish['category_id'] != 5]
    dish_rand = choice(eda)
    dish = get_object_or_404(Dish, id=dish_rand['id'])
    form = CartAddDishForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(dish=dish,
                 quantity=1,
                 override_quantity=cd['override'])
        messages.success(request, f'Товар - "{dish}" добавлен в корзину')
    else:
        messages.error(request, f'Ошибка \n Товар - {dish} не добавлен')
    return redirect('food_order:dish_list')


@require_POST
def cart_add_random_drink(request):
    cart = Cart(request)
    eda = [dish for dish in list(Dish.objects.all().values())
           if dish['category_id'] == 5]
    dish_rand = choice(eda)
    dish = get_object_or_404(Dish, id=dish_rand['id'])
    form = CartAddDishForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(dish=dish,
                 quantity=1,
                 override_quantity=cd['override'])
        messages.success(request, f'Товар - "{dish}" добавлен в корзину')
    else:
        messages.error(request, f'Ошибка \n Товар - {dish} не добавлен')
    return redirect('food_order:dish_list')

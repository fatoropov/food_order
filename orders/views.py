from django.shortcuts import render
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.models import User
from users.views import register


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         dish=item['dish'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart,
                   'form': form})


def get_orders_history(request):
    print(type(request.user))
    if request.user:
        return register(request)
    else:
        client = list(User.objects.filter(id=request.user.id).values())
        orders = [order for order in list(Order.objects.all().values())
                  if order['name_id'] == client[0]['id']]
        orders_id = [id['id'] for id in orders]

        orders_item_sum = {}
        for i in orders_id:
            orders_item_sum[i] = 0
        for item in list(OrderItem.objects.all().values()):
            for i in list(orders_item_sum.keys()):
                if item['order_id'] == i:
                    orders_item_sum[i] += item['price']

        for order in orders:
            if int(order['id']) in list(orders_item_sum.keys()):
                order['price'] = orders_item_sum[int(order['id'])]

        return render(request,
                      'orders/order/history.html',
                      {'orders': orders})

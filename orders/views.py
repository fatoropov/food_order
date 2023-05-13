from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from .send import send_report
import weasyprint


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


@login_required
def get_orders_history(request):

    client = list(User.objects.filter(id=request.user.id).values())
    orders_list = [order for order in list(Order.objects.all().values())
                   if order['name_id'] == client[0]['id']]
    orders_id = [id['id'] for id in orders_list]
    print(orders_list)
    orders_item_sum = {}
    for i in orders_id:
        orders_item_sum[i] = 0
    for item in list(OrderItem.objects.all().values()):
        for i in list(orders_item_sum.keys()):
            print(item)
            if item['order_id'] == i:
                orders_item_sum[i] += item['price'] * item['quantity']
                print(orders_item_sum)

    for order in orders_list:
        if int(order['id']) in list(orders_item_sum.keys()):
            order['price'] = orders_item_sum[int(order['id'])]

    paginator = Paginator(orders_list, 5)
    page_number = request.GET.get('page', 1)
    try:
        orders = paginator.page(page_number)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    return render(request,
                  'orders/order/history.html',
                  {'orders': orders})


def order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
                     settings.STATIC_ROOT / 'css/pdf.css')])
    send_report(request, order_id)
    return redirect('orders:orders_history')

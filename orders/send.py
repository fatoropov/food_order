from io import BytesIO
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


def send_report(request, order_id):
    """
    Задание по отправке уведомления по электронной почте
    при успешной оплате заказа.
    """
    order = Order.objects.get(id=order_id)
    user = request.user
    # содержание письма
    subject = f'Order food - ваш заказ №{order.id}'
    message = 'Пожалуйста, проверьте правильность заказа'
    email = EmailMessage(subject,
                         message,
                         'admin@myshop.com',
                         [user.email])
    # сгенерировать PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,
                                           stylesheets=stylesheets)
    # прикрепить PDF-файл
    email.attach(f'Заказ_№{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    # отправить электронное письмо
    email.send()

from decimal import Decimal
from django.conf import settings
from food_order.models import Dish


class Cart:
    def __init__(self, request):
        """ Инициализировать корзину """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, dish, quantity=1, override_quantity=False):
        """ Добавить товар в корзину и обновляет кол-во """
        dish_id = str(dish.id)
        if dish_id not in self.cart:
            self.cart[dish_id] = {'quantity': 0,
                                  'price': str(dish.price)}
        if override_quantity:
            self.cart[dish_id]['quantity'] = quantity
        else:
            self.cart[dish_id]['quantity'] += quantity
        self.save()

    def save(self):
        """ Сохраняет изменение сеанса """
        self.session.modified = True

    def remove(self, dish):
        """ Удалить товар из корзины """
        dish_id = str(dish.id)
        if dish_id in self.cart:
            del self.cart[dish_id]
            self.save()

    def __iter__(self):
        """ Получает все товары из БД """
        dish_ids = self.cart.keys()
        dishes = Dish.objects.filter(id__in=dish_ids)
        cart = self.cart.copy()
        for dish in dishes:
            cart[str(dish.id)]['dish'] = dish
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """ Считает кол-во товаров в корзине """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item
                   in self.cart.values())

    def clear(self):
        """ Очищает корзину в сеансе """
        del self.session[settings.CART_SESSION_ID]
        self.save()

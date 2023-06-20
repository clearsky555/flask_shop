from django.conf import settings

from src.apps.product.models import Product

from decimal import Decimal


class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart: # если нет корзины в сессиях. Создаем новый в сессии.
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False): # добавление в корзину
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        self.session.modified=True

    def remove(self, product): # удаление товара из корзины
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self): # добавление возможности проводить итерацию над корзиной
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for p in products:
            cart[str(p.id)]['product'] = p

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self): # возвращает количество товаров в корзине
        total_len = 0
        for item in self.cart.values():
            total_len += item['quantity']
        return total_len

    def get_total_price(self):
        total_sum = 0
        for item in self.cart.values():
            total_sum += Decimal(item['price']) * item['quantity']
        return total_sum

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_len(self):
        return len(self)

    def minus(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= 1
            if self.cart[product_id]['quantity'] <= 0:
                del self.cart[product_id]
        self.save()
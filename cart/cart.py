from IMarket import settings
from shop.models import Book
from decimal import Decimal


class Cart(object):
    def __init__(self, request):
        # Ініціалізація корзини користувача
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        # Якщо в даній сесії нема корзини то створюємо її(пусту корзину)
        # А якщо в даній сесії користувача вже існувала корзина
        # то просто ініціалізуємо нашу Cart присвоївши їй вміст вже існуючої
        if not cart:
            # Зберігаємо корзину користувача в сесію
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Book.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_total_price_for_each_product(self):
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

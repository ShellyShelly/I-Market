from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from IMarket import settings
from account.models import User
from cart.cart import Cart
from cart.views import check_cart
from order.forms import MakeOrderForm

# Create your views here.
from order.models import Order, OrderedItem
from order.tokens import order_confirmation_token
from shop.models import Book


class MakeOrder(View):
    def get(self, request):
        cart, flag = check_cart(request)
        if not auth.get_user(request).is_authenticated or flag:
            return redirect('cart:CartDetail')

        form = MakeOrderForm(
            initial={'name': request.user.name,
                     'surname': request.user.surname,
                     'email': request.user.email,
                     'mobile': request.user.mobile,
                     'address': request.user.address,
                     'city': request.user.city,
                     'country': request.user.country,
                     'postal_code': request.user.postal_code,
                     }
        )
        return render(request, 'order/make_order.html', {'form': form, })

    def post(self, request):
        form = MakeOrderForm(request.POST or None)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            cart = Cart(request)
            for item in cart:
                product = get_object_or_404(Book, name=item['product'])
                price = product.price
                quantity = item['quantity']
                ordered_item = OrderedItem(
                    product=product,
                    price=price,
                    quantity=quantity,
                    order=order
                )
                ordered_item.save()

            current_site = get_current_site(request)
            message = render_to_string('order/order_activation_email.html', {
                'user': request.user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(order.pk)),
                'token': order_confirmation_token.make_token(order),
            })
            mail_subject = 'Confirm your order'
            to_email = form.cleaned_data.get('email')
            from_email = settings.EMAIL_HOST_USER
            email = EmailMessage(from_email=from_email, subject=mail_subject, body=message, to=[to_email])
            email.send()
            return render(request, 'order/email_is_sent.html')

        return redirect('shop:ProductList')


def confirm_order(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        order = Order.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        order = None
    if order is not None and order_confirmation_token.check_token(order, token):
        order.is_confirmed = True
        items = OrderedItem.objects.filter(order=order.pk)
        for item in items:
            product_on_stock = get_object_or_404(Book, pk=item.product.pk)
            product_on_stock.count = product_on_stock.count - item.quantity
            product_on_stock.save()
        order.save()
        return render(request, 'order/order_confirmation_is_successful.html')
    else:
        return render(request, 'order/confirmation_link_is_invalid.html')

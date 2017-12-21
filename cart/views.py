from django.contrib import auth
from django.shortcuts import render, get_object_or_404, redirect
from cart.cart import Cart
from .forms import AddProductToCartForm
from django.views.decorators.http import require_POST
from shop.models import Book


def check_cart(request):
    cart = Cart(request)
    flag = False
    for item in cart:
        product = get_object_or_404(Book, name=item['product'])
        if product.count < item['quantity']:
            flag = True
            error_msg = 'Доступно для замовлення лише {}'.format(product.count)
            item['error_msg'] = error_msg
        item['update_quantity_form'] = AddProductToCartForm(
            initial={
                'quantity': item['quantity'],
                'update': True
            })
    return cart, flag


# Create your views here.
def cart_detail(request):
    error_message = None
    cart, flag = check_cart(request)
    if not auth.get_user(request).is_authenticated:
        error_message = 'Sorry. You should login first!'
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'error_message': error_message})


@require_POST
def add_product_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Book, id=product_id)
    form = AddProductToCartForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    # return render(request, 'cart/add_product_to_cart.html', {'cart': cart, 'form': form})
    return redirect('cart:CartDetail')


def add_product_to_cart_no_id(request):
    cart = Cart(request)
    form = AddProductToCartForm(request.POST)
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'form': form})


def remove_product_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Book, pk=product_id)
    cart.remove(product)
    return redirect('cart:CartDetail')


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:CartDetail')


def purchase(request):
    cart = Cart(request)
    flag = False
    for item in cart:
        product = get_object_or_404(Book, name=item['product'])
        if product.count < item['quantity']:
            error_msg = 'Доступно для замовлення лише {}'.format(product.count)
            item['error_msg'] = error_msg
            flag = True

    if flag:
        for item in cart:
            item['update_quantity_form'] = AddProductToCartForm(
                initial={
                    'quantity': item['quantity'],
                    'update': True
                })
        return render(request, 'cart/cart_detail.html', {'cart': cart})

    return redirect('order:MakeOrder')

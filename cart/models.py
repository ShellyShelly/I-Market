"""
from django.db import models
from shop.models import Book
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


class Item(models.Model):
    cart = models.ForeignKey(Cart)
    item = models.ForeignKey(Book)
    quantity = models.PositiveIntegerField(verbose_name='К-сть')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна за одиницю товару')

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'
        ordering = ('cart',)


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User)
    session = models.ForeignKey(Session)
    creation_date = models.DateTimeField(verbose_name='Час та дата створення')
    checked_out = models.BooleanField(default=False, verbose_name='IS checked out')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзини'
        ordering = ['creation_date', ]

"""

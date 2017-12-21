from django.db import models
from account.models import User
from shop.models import Book


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(verbose_name='Postal code', max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=12, blank=True, null=True)
    is_paid = models.BooleanField(verbose_name='Is paid', default=False)
    date_of_creation = models.DateTimeField(verbose_name='Date of creation', auto_now_add=True)
    is_confirmed = models.BooleanField(verbose_name='Is confirmed', default=False)

    class Meta:
        ordering = ('-date_of_creation', )
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

    def __str__(self):
        return 'Order: {}'.format(self.id)


class OrderedItem(models.Model):
    order = models.ForeignKey(Order, related_name='Items')
    product = models.ForeignKey(Book, related_name='Books')
    price = models.DecimalField(verbose_name='Prices', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='Quantities', default=1)

    def __str__(self):
        return '{}'.format(self.product)

    def get_cost(self):
        return self.price * self.quantity

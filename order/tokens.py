from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class OrderConfirmationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, order, timestamp):
        return (six.text_type(order.pk) + six.text_type(timestamp)) + six.text_type(order.is_confirmed)


order_confirmation_token = OrderConfirmationTokenGenerator()
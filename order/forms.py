from django import forms

from order.models import Order


class MakeOrderForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    surname = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    mobile = forms.CharField(max_length=12)
    address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255)
    country = forms.CharField(max_length=255)
    postal_code = forms.CharField(max_length=10)

    class Meta:
        model = Order
        exclude = ('user', 'is_paid', 'date_of_creation', 'is_confirmed')
        fields = ['name', 'surname', 'email', 'mobile', 'address', 'city', 'country', 'postal_code']

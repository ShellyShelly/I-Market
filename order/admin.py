from django.contrib import admin

# Register your models here.
from order.models import Order, OrderedItem


class OrderedItemInline(admin.TabularInline):
    model = OrderedItem
    raw_id_field = ['name']


class OrderAdmin(admin.ModelAdmin):
    model = Order
    fieldsets = (
        ('User', {'fields': ('user', )}),
        ('Information about delivering', {'fields': ('mobile', 'address', 'city', 'country', 'postal_code')}),
        ('Information about order', {'fields': ('is_paid', 'is_confirmed', 'date_of_creation')}),
    )
    readonly_fields = ('user', 'date_of_creation', 'is_confirmed')
    ordering = ('user', 'is_paid', 'is_confirmed', 'date_of_creation')
    list_display = ['user', 'is_paid', 'is_confirmed', 'date_of_creation']
    list_filter = ['is_confirmed', 'is_paid', 'date_of_creation']
    inlines = [OrderedItemInline]


admin.site.register(Order, OrderAdmin)

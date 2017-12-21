from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .forms import UserAdminCreationForm, UserAdminEditForm
from .models import User


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminEditForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'surname', 'admin', 'staff', 'active')
    list_filter = ('admin',  'staff', 'active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'mobile')}),
        ('Account info', {'fields': ('confirmation_date', 'last_login')}),
        ('Personal info', {'fields': ('name', 'surname', 'address', 'city', 'country', 'postal_code')}),
        ('Permissions', {'fields': ('admin', 'staff', 'active')}),
    )
    readonly_fields = ('last_login', 'confirmation_date')
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'name', 'surname')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)


# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

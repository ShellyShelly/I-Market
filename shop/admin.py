from django.contrib import admin
from .models import Category, Author, Book


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'


class AuthorAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'


# make be able to don`t fill some fields as year of published and etc.
class BookAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('name', 'author_full_name')

    def author_full_name(self, obj):
        return obj.author.name + ' ' + obj.author.surname


admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)

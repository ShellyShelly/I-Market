from django.db import models
from django.core.urlresolvers import reverse


class Category(models.Model):
    name = models.CharField(max_length=120)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:ProductListByCategory', args=[str(self.id)])


# add field with whole date of birth and death
class Author(models.Model):
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120, blank=True)
    year_of_birth = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    year_of_death = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name + ' ' + self.surname

    class Meta:
        ordering = ['name', 'surname']
        verbose_name = 'Автор'
        verbose_name_plural = 'Автори'

    def get_absolute_url(self):
        return reverse('shop:AuthorDetail', args=[str(self.id)])


# not finished yet!
class Book(models.Model):
    name = models.CharField(max_length=120, db_index=True)
    author = models.ForeignKey(Author, related_name='author_books')
    category = models.ForeignKey(Category)
    year_of_published = models.DecimalField(max_digits=4, decimal_places=0, blank=True)
    count = models.DecimalField(max_digits=5, decimal_places=0)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='books', blank=True, verbose_name="Зображення книги")
    # rating -- make later

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def get_absolute_url(self):
        return reverse('shop:BookDetail', args=[str(self.id)])

"""
from django.db import models


class SearchManager(models.Manager):
    def search(self, **kwargs):
        qs = self.get_query_set()
        if kwargs.get('q', ''):
            qs = qs.filter(name__icontains=kwargs['q'])
        if kwargs.get('author', []):
            qs = qs.filter(author=kwargs['author'])
        return qs
"""

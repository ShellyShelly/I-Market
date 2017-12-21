from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Book, Category, Author
from cart.forms import AddProductToCartForm

"""
!!!!!!!!!!!!!!!!
переглянути пізніше
!!!!!!!!!!!!!!!!
попробувати реалізувати так само
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



# views.py
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from shop.models import Book, Publisher

class PublisherBookList(ListView):

    template_name = 'shop/books_by_publisher.html'

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, name=self.args[0])
        return Book.objects.filter(publisher=self.publisher)
"""


# Create your views here.
"""
function-based view
"""


# make better sorting! beacause words that start from 'i' are closer than 'a' in ru and ua
# make showing olny a few products and categories and add buttons to show more or scrolling
def index_page_view(request, category_id=None):
    category = None
    categories = Category.objects.all()[:]
    products = Book.objects.all()

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)

    return render(request, 'shop/index_page.html', {
        'category': category,
        'categories': categories,
        'products': products
    })


def book_detail_view(request, pk):
    product = get_object_or_404(Book, pk=pk)
    categories = Category.objects.all()[:]
    cart_product_form = AddProductToCartForm()

    return render(request, 'shop/book_detail.html', {
        'categories': categories,
        'object': product,
        'cart_product_form': cart_product_form,
    })


"""
class-based view
"""


class IndexPageView(ListView):
    model = Book
    template_name = 'shop/index_page.html'

    def get_context_data(self, **kwargs):
        queryset = ''
        context = super(IndexPageView, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['products'] = Book.objects.all()
        category_id = None
        try:
            category_id = self.kwargs["category_id"]
            category = get_object_or_404(Category, id=category_id)
            context['products'] = context['products'].filter(category=category)
        except KeyError:
            category = None

        paginator = Paginator(context['products'], 3)
        page_request_var = "page"
        page = self.request.GET.get(page_request_var)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        context['category'] = category
        context['products'] = queryset
        context['page_request_var'] = page_request_var
        return context


"""
class BookDetailView(DetailView):
    model = Book
    template_name = 'shop/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data()
        context['object'] = get_object_or_404(Book, pk=self.kwargs['pk'])
        cart_product_form = AddProductToCartForm()
        context['cart_product_form '] = cart_product_form
        return context


"""


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'shop/author_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data()
        context['object'] = get_object_or_404(Author, pk=self.kwargs['pk'])
        related_products = Book.objects.filter(author=context['object'])

        paginator = Paginator(related_products, 2)
        page_request_var = "page"
        page = self.request.GET.get(page_request_var)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        context['page_request_var'] = page_request_var
        context['related_products'] = queryset
        return context



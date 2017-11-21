from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from shop.models import Book


# Create your views here.
def searched_info(request):
    queryset_list = Book.objects.all()
    query = request.GET.get("query")
    queryset = ''
    page_request_var = 1
    message = ""
    if query:
        queryset_list = queryset_list.filter(name__icontains=query) | \
                        queryset_list.filter(author__name__icontains=query) | \
                        queryset_list.filter(author__surname__icontains=query)

        page_request_var = "page"
        page = request.GET.get(page_request_var)
        paginator = Paginator(queryset_list, 3)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
    else:
        message = 'Your search query is empty:)'
    context = {
        "object_list": queryset,
        "page_request_var": page_request_var,
        "query": query,
        "message": message,
    }

    return render(request, "search/searched_info.html", context)

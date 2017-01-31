from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import ListView, DetailView
from django.conf import settings
from datetime import date
from .models import Product

class Index(ListView):
    template_name = 'commerce/index.html'
    page_len = 12

    def get_queryset(self):
        # for value reuse in context method
        self.num_products = Product.objects.count()

        # kwargs always has page key
        page = self.kwargs['page']
        if page is not None:
            page = int(page)
        else:
            page = 1

        start = (page - 1) * Index.page_len
        if start >= self.num_products:
            raise Http404()

        return Product.objects.all()[start:start+Index.page_len]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = self.kwargs['page']

        num_pages = (self.num_products // Index.page_len)
        num_pages += (1 if self.num_products % Index.page_len != 0 else 0)
        context['num_pages'] = num_pages

        return context

class Details(DetailView):
    model = Product
    template_name = 'commerce/product.html'

def login(request):
    raise Http404('Cannot login at this time')

def logout(request):
    raise Http404('Cannot logout at this time')

def add(request, pk):
    raise Http404('Cannot add product at this time.')

def cart(request):
    raise Http404('Cannot view cart at this time.')

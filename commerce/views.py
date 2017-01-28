from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import ListView, DetailView
from django.conf import settings
from datetime import datetime
from .models import Product

class Index(ListView):
    template_name = 'commerce/index.html'

    def get_queryset(self):
        set_len = 10
        num_products = Product.objects.count()

        # kwargs always has page key
        page = self.kwargs['page']
        if page is not None:
            page = int(page)
        else:
            page = 1

        start = (page - 1) * set_len
        if start >= num_products:
            raise Http404()

        return Product.objects.all()[start:start+set_len]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_name'] = settings.SITE_NAME

        return context

class Details(DetailView):
    model = Product
    template_name = 'commerce/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_name'] = settings.SITE_NAME

        return context

def login(request):
    raise Http404('Cannot login at this time')

def logout(request):
    raise Http404('Cannot logout at this time')

def add(request, pk):
    raise Http404('Cannot add product at this time.')

def cart(request):
    raise Http404('Cannot view cart at this time.')

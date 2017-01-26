from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_safe
from datetime import datetime
from .models import Product

@require_safe
def index(request):
    q = Product.objects.all()[:10]
    context = {
        'product_list': q,
    }

    return render(request, 'commerce/index.html', context=context)

@require_safe
def product(request, pk):
    content = ''

    try:
        content = Product.objects.get(pk=pk)
    except Product.DoesNotExist as e:
        content = e
    finally:
        return HttpResponse(content)

def login(request):
    raise Http404('Cannot login at this time')

def logout(request):
    raise Http404('Cannot logout at this time')

def add(request, pk):
    raise Http404('Cannot add product at this time.')

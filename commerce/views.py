from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Product
from datetime import datetime

def index(request):
    html = (
        '<!DOCTYPE html>'
        '<html>'
        '<body>'
        '<p>This is the CompMart index!</p>'
        '<p>The time is {}.</p>'.format(datetime.now()) +
        '</body>'
        '</html>'
    )

    return HttpResponse(html)

def product(request, pk='1'):
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

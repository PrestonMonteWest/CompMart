from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from .models import Product

def index(request):
    content = (
        '<!DOCTYPE html>'
        '<html>'
        '<body>'
        '<p>This is the CompMart index!</p>'
        '<p>The time is {}.</p>'.format(timezone.now()) +
        '</body>'
        '</html>'
    )

    return HttpResponse(content)

def product(request, pk='1'):
    content = ''

    try:
        content = Product.objects.get(pk=pk)
    except Product.DoesNotExist as e:
        content = e
    finally:
        return HttpResponse(content)

def login(request):
    return HttpResponse('login page')

def logout(request):
    return HttpResponse('logout page')

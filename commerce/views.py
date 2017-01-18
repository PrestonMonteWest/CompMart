from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse

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

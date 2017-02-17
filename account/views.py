from django.shortcuts import reverse, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_safe
from commerce import get_cart

@require_safe
@login_required
def index(request):
    return render(request, 'account/index.html')

@require_safe
def logout(request):
    cart = get_cart(request.session)
    auth_logout(request)
    request.session['cart'] = cart
    url = request.GET.get('next', reverse('index'))
    return redirect(url)


from django.shortcuts import reverse, redirect
from django.views.decorators.http import require_safe
from commerce import get_cart

@require_safe
def logout(request):
    cart = get_cart(request.session)
    auth.logout(request)
    request.session['cart'] = cart
    url = request.GET.get('next', reverse('index'))
    return redirect(url)


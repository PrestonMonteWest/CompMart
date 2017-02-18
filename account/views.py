from django.shortcuts import reverse, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_safe, require_http_methods
from django.core.urlresolvers import resolve, reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import password_change, login
from commerce import get_cart
from .forms import AddressForm
from .models import Address, CreditCard

password_change.login_required = True
login.login_required = False

@require_safe
@login_required
def index(request):
    return render(request, 'account/index.html')

index.login_required = True

@require_safe
def logout(request):
    cart = get_cart(request.session)
    auth_logout(request)
    request.session['cart'] = cart
    url = request.GET.get('next', reverse('index'))
    if resolve(url).func.login_required:
        url = reverse('index')

    return redirect(url)

logout.login_required = False

class Register(CreateView):
    template_name = 'account/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')

    @classmethod
    def as_view(cls):
        view = super().as_view()
        view.login_required = False
        return view

@require_http_methods(['HEAD', 'GET', 'POST'])
@login_required
def add_address(request, success=False):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            Address.objects.create(user=request.user, **form.cleaned_data)
            return redirect(reverse('account:add_address_done'))
    else:
        form = AddressForm()

    context = {
        'success': success,
        'form': form,
    }

    return render(request, 'account/add_address.html', context=context)

add_address.login_required = True

@require_http_methods(['HEAD', 'GET', 'POST'])
@login_required
def view_addresses(request):
    pass

view_addresses.login_required = True

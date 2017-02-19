from django.shortcuts import reverse, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import resolve, reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .forms import AddressForm, CreditCardForm
from .models import Address, CreditCard

from django.contrib.auth.views import password_change, login
password_change.login_required = True
login.login_required = False

@login_required
def index(request):
    address_count = Address.objects.count()
    card_count = CreditCard.objects.count()
    links = []
    if address_count:
        links.append({
            'name': 'Addresses',
            'href': reverse('account:addresses'),
        })
    else:
        links.append({
            'name': 'Add Address',
            'href': reverse('account:add_address'),
        })

    if card_count:
        links.append({
            'name': 'Cards',
            'href': reverse('account:cards'),
        })
    else:
        links.append({
            'name': 'Add Card',
            'href': reverse('account:add_card'),
        })

    return render(request, 'account/index.html', {'links': links})

index.login_required = True

def logout(request):
    from django.contrib.auth import logout as auth_logout
    from commerce import get_cart
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

@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            try:
                Address.objects.create(user=request.user, **form.cleaned_data)
                return redirect(reverse('account:addresses'))
            except IntegrityError:
                form.add_error(
                    None,
                    ValidationError('This address already exists!')
                )
    else:
        form = AddressForm()

    return render(request, 'account/add_address.html', {'form': form})

add_address.login_required = True

@login_required
def edit_address(request, pk):
    pass

edit_address.login_required = True

@login_required
def delete_address(request, pk):
    pass

delete_address.login_required = True

@login_required
def add_card(request):
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():
            try:
                CreditCard.objects.create(user=request.user, **form.cleaned_data)
                return redirect(reverse('account:cards'))
            except IntegrityError:
                form.add_error(
                    None,
                    ValidationError('This credit card already exists!')
                )
    else:
        form = CreditCardForm()

    return render(request, 'account/add_card.html', {'form': form})

add_card.login_required = True

@login_required
def edit_card(request, pk):
    pass

edit_card.login_required = True

@login_required
def delete_card(request, pk):
    pass

delete_card.login_required = True

class AddressList(ListView):
    template_name = 'account/addresses.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        return self.request.user.addresses.all()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @classmethod
    def as_view(cls):
        view = super().as_view()
        view.login_required = True
        return view

class CardList(ListView):
    template_name = 'account/cards.html'
    context_object_name = 'cards'

    def get_queryset(self):
        return self.request.user.cards.all()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @classmethod
    def as_view(cls):
        view = super().as_view()
        view.login_required = True
        return view

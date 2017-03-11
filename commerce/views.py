from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.db import transaction
from django.db.models import Q
from django.forms import ValidationError
from account import login_required
from account.models import Address, CreditCard
from .forms import ProductSearchForm, CheckoutForm
from .models import Product, OrderItem, Order
from . import get_cart

def get_products(session):
    cart = get_cart(session)
    products = {}
    errors = []
    for pk in sorted(cart):
        try:
            products[pk] = Product.active_objects.get(pk=pk)
        except Product.DoesNotExist:
            del cart[pk]
            session.modified = True
            errors.append(
                ValidationError(
                    'A product has been removed from your cart '
                    'because it is now ineligible for purchase.'
                )
            )

    return (products, errors)

class Index(ListView):
    template_name = 'commerce/index.html'
    context_object_name = 'products'
    page_len = 12

    def get_queryset(self):
        if 'query' in self.request.GET:
            self.search = ProductSearchForm(self.request.GET, auto_id=False)
        else:
            self.search = ProductSearchForm(auto_id=False)

        if self.search.is_valid():
            # emulate keyword-searching against database using Q objects
            terms = self.search.cleaned_data['query'].split()
            query = Q(name__icontains=terms.pop())
            for term in terms:
                query |= Q(name__icontains=term)

            products = Product.active_objects.filter(query)
        else:
            products = Product.active_objects.all()

        self.num_products = products.count()

        # page for pagination
        page = self.kwargs.get('page', None)
        if page is not None:
            self.page = int(page)
        else:
            self.page = 1

        self.num_pages = (self.num_products // self.page_len)
        self.num_pages += (1 if self.num_products % self.page_len != 0 else 0)

        if self.num_pages != 0 and self.page > self.num_pages:
            raise Http404()

        start = (self.page - 1) * self.page_len
        return products[start:start+self.page_len]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = self.page
        context['form'] = self.search
        context['num_pages'] = self.num_pages
        context['page_iter'] = range(self.num_pages)

        return context

class ProductDetails(DetailView):
    model = Product
    template_name = 'commerce/product.html'

def add_product(request, pk):
    try:
        product = Product.active_objects.get(pk=pk)
    except Product.DoesNotExist:
        pass
    else:
        cart = get_cart(request.session)
        stock = product.stock
        if pk in cart and stock > cart[pk]:
            cart[pk] += 1
        elif pk not in cart and stock > 0:
            cart[pk] = 1

        request.session.modified = True

    url = request.GET.get('next', reverse('index'))
    return redirect(url)

def delete_product(request, pk):
    cart = get_cart(request.session)
    if pk in cart:
        del cart[pk]
        request.session.modified = True

    url = request.GET.get('next', reverse('index'))
    return redirect(url)

def cart(request):
    products, errors = get_products(request.session)
    cart = get_cart(request.session)
    if request.method == 'POST' and not errors:
        post = request.POST.copy()
        if 'checkout' in post:
            checkout = True
            del post['checkout']
        else:
            checkout = False

        for key, value in post.items():
            if key not in cart:
                    continue

            product = products[key]
            stock = product.stock
            try:
                value = int(value)
            except ValueError:
                continue

            if value > stock:
                value = stock

            if value >= 1:
                cart[key] = value
                request.session.modified = True

        if checkout and cart:
            return redirect(reverse('commerce:checkout'))

    items = []
    total = 0
    for product in products.values():
            quantity = cart[str(product.pk)]
            total += product.price * quantity
            items.append({
                'product': product,
                'quantity': quantity,
            })

    context = {
        'total': total,
        'items': items,
        'errors': errors,
    }

    return render(request, 'commerce/cart.html', context)

@login_required
def checkout(request):
    products, errors = get_products(request.session)
    cart = get_cart(request.session)
    if not cart:
        if not errors:
            return redirect(reverse('index'))

        return render(
            request,
            'commerce/cart.html',
            {'errors': errors},
        )

    addresses = request.user.addresses.all()
    if not addresses:
        return redirect('{}?next={}'.format(
            reverse('account:add_address'),
            request.path
        ))

    cards = request.user.cards.all()
    if not cards:
        return redirect('%s?next=%s' % (
            reverse('account:add_card'),
            request.path
        ))

    form = CheckoutForm(
        request.POST or None,
        cards=cards,
        addresses=addresses,
    )

    for error in errors:
        form.add_error(None, error)

    if form.is_valid():
        address = Address.objects.get(pk=form.cleaned_data['address'])
        card = CreditCard.objects.get(pk=form.cleaned_data['card'])
        order = Order(
            user=request.user,
            card=card,
            street=address.street,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
        )

        items = []
        total = 0
        for pk, product in products.items():
            price = product.price
            items.append(OrderItem(
                product=product,
                order=order,
                purchase_price=price,
                quantity=cart[pk],
            ))
            total += price

        order.total = total
        try:
            with transaction.atomic():
                order.save()
                for item in items:
                    item.save()
        except ValueError as e:
            form.add_error(None, ValidationError(str(e)))
        else:
            # charge credit card
            cart.clear()
            request.session.modified = True
            return redirect(reverse('commerce:thank_you', args=(order.pk,)))

    return render(request, 'commerce/checkout.html', {'form': form})

@login_required
def thank_you(request, pk):
    pass

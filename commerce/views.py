from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from account import login_required
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
        if 'checkout' in request.POST:
            checkout = True
            del request.POST['checkout']
        else:
            checkout = False

        for key, value in request.POST.items():
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
    cart = get_cart(request.session)
    if not cart:
        return redirect(reverse('index'))

    cards = request.user.cards.all()
    if not cards:
        return redirect('{}?next={}'.format(
            reverse('account:add_card'),
            request.path
        ))

    addresses = request.user.addresses.all()
    if not addresses:
        return redirect('{}?next={}'.format(
            reverse('account:add_address'),
            request.path
        ))

    form = CheckoutForm(request.POST or None, cards=cards, addresses=addresses)
    products, errors = get_products(request.session)
    for error in errors:
        form.add_error(None, error)

    if form.is_valid():
        order = Order(user=request.user)
        items = []
        total = 0
        for product in products:
            items.append(OrderItem(
                product=product,
                order=order,
                price=product.price,
                quantity=quantity
            ))
            total += product.price

        order.total = total
        order.save()
        for item in items:
            item.save()

        return redirect(reverse('commerce:thank_you', args=(order.pk,)))

    return render(request, 'commerce/checkout.html', {'form': form})

@login_required
def thank_you(request, pk):
    pass

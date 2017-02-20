from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from account import login_required
from .forms import ProductSearchForm
from .models import Product
from . import get_cart

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

        start = (self.page - 1) * self.page_len
        return products[start:start+self.page_len]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = self.page
        context['form'] = self.search

        num_pages = (self.num_products // self.page_len)
        num_pages += (1 if self.num_products % self.page_len != 0 else 0)
        context['num_pages'] = num_pages
        context['page_iter'] = range(num_pages)

        return context

class ProductDetails(DetailView):
    model = Product
    template_name = 'commerce/product.html'

    def get_object(self, queryset=None):
        product = super().get_object(queryset)
        if product.discontinued:
            raise Http404()

        return product

def add_product(request, pk):
    get_object_or_404(Product, pk=pk)
    cart = get_cart(request.session)

    if pk in cart:
        cart[pk] += 1
    else:
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
    cart = get_cart(request.session)
    if request.method == 'POST':
        for key, value in request.POST.items():
            try:
                pk = key
                value = int(value)
                if value >= 1:
                    cart[pk] = value
                    request.session.modified = True

            except (KeyError, ValueError):
                pass

        if 'checkout' in request.POST:
            return redirect(reverse('commerce:checkout'))

    items = []
    total = 0
    for pk in sorted(cart):
        try:
            product = Product.active_objects.get(pk=pk)
        except Product.DoesNotExist:
            del cart[pk]
            request.session.modified = True
            continue
        else:
            quantity = cart[pk]
            total += product.price * quantity
            items.append({
                'product': product,
                'quantity': quantity,
            })

    context = {
        'total': total,
        'items': items,
    }

    return render(request, 'commerce/cart.html', context)

@login_required
def checkout(request):
    cards = request.user.cards.all()
    if not cards:
        return redirect('account:add_card')
    elif request.method == 'POST':
        # process post data
        return redirect('commerce:thank_you')

    # display form

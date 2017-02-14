from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_http_methods, require_safe
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from .models import Product
from .forms import ProductSearchForm

def get_cart(session):
    '''
    Given a Django session, if the cart exists return it,
    otherwise return an empty cart
    '''

    if 'cart' not in session:
        session['cart'] = {}

    return session['cart']

class Index(ListView):
    template_name = 'commerce/index.html'
    context_object_name = 'products'
    page_len = 12

    def get_queryset(self):
        # determine if the request is from a search form submission
        # if it is, bind it
        self.search = ProductSearchForm(auto_id=False)
        for key in self.request.GET:
            if key in self.search.declared_fields:
                self.search = ProductSearchForm(
                    self.request.GET,
                    auto_id=False
                )

                break

        if self.search.is_valid():
            # emulate keyword searching against database using Q objects
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

class Details(DetailView):
    model = Product
    template_name = 'commerce/product.html'

    def get_object(self, queryset=None):
        product = super().get_object(queryset)
        if product.discontinued:
            raise Http404()

        return product

@require_safe
def logout(request):
    cart = get_cart(request.session)
    auth.logout(request)
    request.session['cart'] = cart
    url = request.GET.get('next', reverse('index'))
    return redirect(url)

@require_safe
def add(request, pk):
    get_object_or_404(Product, pk=pk)
    cart = get_cart(request.session)

    if pk in cart:
        cart[pk] += 1
    else:
        cart[pk] = 1

    request.session.modified = True
    url = request.GET.get('next', reverse('index'))
    return redirect(url)

@require_http_methods(['HEAD', 'GET', 'POST'])
def cart(request):
    cart = get_cart(request.session)

    if request.method == 'POST':
        post = request.POST.copy()
        keys = []
        for key, value in post.items():
            if 'update' in key:
                try:
                    pk = key.split('.')[-1]
                    value = int(value)

                    if value >= 1:
                        cart[pk] = value
                        request.session.modified = True

                except (KeyError, ValueError):
                    pass

                keys.append(key)

        for key in keys:
            del post[key]

        if 'checkout' in post:
            return redirect(reverse('commerce:checkout'))

        for key, value in post.items():
            if value == 'Delete':
                try:
                    del cart[key]
                except ValueError:
                    pass
                else:
                    request.session.modified = True
                    break

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

    return render(request, 'commerce/cart.html', context=context)

class Register(CreateView):
    template_name = 'commerce/register.html'
    form_class = UserCreationForm
    success_url = '/'

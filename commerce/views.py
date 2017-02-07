from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_http_methods, require_safe
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.http import Http404
from django.views.generic import ListView, DetailView
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

def flatten_errors(form):
    '''
    Given a Form class, flatten form errors into a single list
    '''

    errors = []
    for input_element in form:
        errors.extend(input_element.errors)

    return errors

class Index(ListView):
    template_name = 'commerce/pages/index.html'
    page_len = 12

    def get_queryset(self):
        # for value reuse in context method
        self.num_products = Product.objects.count()

        # kwargs always has page key
        page = self.kwargs.get('page', None)
        if page is not None:
            self.page = int(page)
        else:
            self.page = 1

        start = (self.page - 1) * self.page_len
        if start >= self.num_products:
            raise Http404()

        # determine if the request is from a search form submission
        # if it is, bind it
        self.search = ProductSearchForm(auto_id=False)
        for key in self.request.GET:
            if key in self.search.declared_fields:
                self.search = ProductSearchForm(self.request.GET, auto_id=False)
                break

        if self.search.is_valid():
            # emulate keyword searching against database using Q objects
            terms = self.search.cleaned_data['query'].split()
            query = Q(name__icontains=terms.pop())
            for term in terms:
                query |= Q(name__icontains=term)

            products = Product.objects.filter(query)
        else:
            products = Product.objects.all()

        return products[start:start+self.page_len]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = self.page
        context['form'] = self.search
        context['errors'] = flatten_errors(self.search)

        num_pages = (self.num_products // self.page_len)
        num_pages += (1 if self.num_products % self.page_len != 0 else 0)
        context['num_pages'] = num_pages

        return context

class Details(DetailView):
    model = Product
    template_name = 'commerce/pages/product.html'

@require_http_methods(['GET', 'POST'])
def login(request):
    template_name = 'commerce/pages/login.html'
    if request.method != 'POST':
        return render(request, template_name, context={
            'errors': [],
        })

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    if user:
        auth_login(request, user)
        return redirect(reverse('index'))
    else:
        return render(request, template_name, context={
            'errors': [
                'Invalid credential combination!',
            ],
            'username': username,
        })

@require_safe
def logout(request):
    cart = get_cart(request.session)
    auth_logout(request)
    request.session['cart'] = cart
    return redirect(reverse('index'))

@require_safe
def add(request, pk):
    get_object_or_404(Product, pk=pk)
    cart = get_cart(request.session)

    if pk in cart:
        cart[pk] += 1
    else:
        cart[pk] = 1

    request.session.modified = True
    return redirect(reverse('index'))

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
            product = Product.objects.get(pk=pk)
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

    return render(request, 'commerce/pages/cart.html', context=context)

def register(request):
    raise Http404('Cannot register at this time.')

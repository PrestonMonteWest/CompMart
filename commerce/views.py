from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_safe
from django.shortcuts import reverse
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.http import Http404
from django.views.generic import ListView, DetailView
from .models import Product

class Index(ListView):
    template_name = 'commerce/index.html'
    page_len = 12

    def get_queryset(self):
        # for value reuse in context method
        self.num_products = Product.objects.count()

        # kwargs always has page key
        page = self.kwargs['page']
        if page is not None:
            page = int(page)
        else:
            page = 1

        start = (page - 1) * Index.page_len
        if start >= self.num_products:
            raise Http404()

        return Product.objects.all()[start:start+Index.page_len]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = self.kwargs['page']

        num_pages = (self.num_products // Index.page_len)
        num_pages += (1 if self.num_products % Index.page_len != 0 else 0)
        context['num_pages'] = num_pages

        return context

class Details(DetailView):
    model = Product
    template_name = 'commerce/product.html'

@require_http_methods(['GET', 'POST'])
def login(request):
    template_name = 'commerce/login.html'
    if request.method != 'POST':
        return render(request, template_name, context={
            'errors': (),
        })

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    if user:
        auth_login(request, user)
        return redirect(reverse('commerce:index'))
    else:
        return render(request, template_name, context={
            'errors': (
                'Invalid credential combination!',
            ),
            'username': username,
        })

@require_safe
def logout(request):
    auth_logout(request)
    return redirect(reverse('commerce:index'))

@require_safe
def add(request, pk):
    try:
        Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        raise Http404()
    else:
        if pk in request.session:
            request.session[pk] += 1
        else:
            request.session[pk] = 1

        return redirect(reverse('commerce:index'))

@require_http_methods(['GET', 'POST'])
def cart(request):
    if request.method == 'POST':
        post = request.POST.copy()
        keys = []
        for key, value in post.items():
            if 'update' in key:
                try:
                    pk = key.split('.')[-1]
                    value = int(value)

                    if value >= 1:
                        request.session[pk] = value

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
                    del request.session[key]
                except ValueError:
                    pass
                else:
                    break

    items = []
    total = 0

    for pk in request.session.keys():
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            del request.session[pk]
            continue
        else:
            quantity = request.session[pk]
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

def register(request):
    raise Http404('Cannot register at this time.')

import datetime
from decimal import Decimal
from django.test import TestCase
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from .. import models

class TestViews(TestCase):
    def setUp(self):
        User.objects.create_user(
            pk=1,
            username='user_1',
            password='password_1',
        )

        user = User.objects.create_user(
            pk=2,
            username='user_2',
            password='password_2',
            is_staff=True,
        )
        user.addresses.create(
            pk=1,
            street='street_1',
            city='city_1',
            state='S1',
            zip_code='zip_1',
        )
        user.cards.create(
            pk=1,
            card_number='',
            card_type='type_1',
            holder_name='name_1',
            expiration_date=datetime.date.today(),
        )

        user = User.objects.create_user(
            pk=3,
            username='user_3',
            password='password_3',
        )
        address = user.addresses.create(
            pk=2,
            street='street_2',
            city='city_2',
            state='S2',
            zip_code='zip_2',
        )
        user.orders.create(
            pk=1,
            street=address.street,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
            total=0,
        )

        prices = [
            '5.99',
            '24.75',
            '19.34',
            '9.23',
            '117.06',
            '29.98',
            '87.34',
            '4.78',
            '0.67',
            '79.98',
            '30.00',
            '69.47',
            '7.99',
            '403.01',
            '71.59',
        ]

        stocks = [
            45,
            3,
            0,
            17,
            98,
            335,
            28,
            49,
            15,
            87,
            164,
            52,
            11,
            96,
            0,
        ]

        for i in range(1, 16):
            models.Product.objects.create(
                pk=i,
                name='product_%d' % i,
                price=prices[i - 1],
                description='',
                stock=stocks[i - 1],
                image='product_%d.jpg' % i,
            )

        product = models.Product.objects.get(pk=1)
        product.description = '%s description' % product.name
        product.save()

        product = models.Product.objects.get(pk=15)
        product.discontinued = True
        product.save()

        self.page_len = 12

        site = Site.objects.get(pk=2)
        site.domain = 'localhost'
        site.name = 'CompMart'
        site.save()

    ### Navigation Tests ###
    def test_nav_no_login(self):
        '''
        Test navigation bar with no login session.
        '''

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Home', count=1)
        self.assertContains(response, 'Cart', count=1)
        self.assertContains(response, 'Login', count=1)
        self.assertContains(response, 'Register', count=1)
        self.assertNotContains(response, 'Logout')
        self.assertNotContains(response, 'Account')
        self.assertNotContains(response, 'Admin')

    def test_nav_login(self):
        '''
        Test navigation bar with login session.
        '''

        user = User.objects.get(username='user_1')
        self.client.force_login(user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Home', count=1)
        self.assertContains(response, 'Cart', count=1)
        self.assertNotContains(response, 'Login')
        self.assertNotContains(response, 'Register')
        self.assertContains(response, 'Logout', count=1)
        self.assertContains(response, 'Account', count=1)
        self.assertNotContains(response, 'Admin')

    def test_nav_login_admin(self):
        '''
        Test navigation bar with admin login session.
        '''

        user = User.objects.get(username='user_2')
        self.client.force_login(user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Home', count=1)
        self.assertContains(response, 'Cart', count=1)
        self.assertNotContains(response, 'Login')
        self.assertNotContains(response, 'Register')
        self.assertContains(response, 'Logout', count=1)
        self.assertContains(response, 'Account', count=1)
        self.assertContains(response, 'Admin', count=1)

    ### Index Tests ###
    def test_index(self):
        '''
        Test index view with no query.
        '''

        products = models.Product.active_objects.all()[:self.page_len]
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['products'], map(repr, products))
        self.assertContains(response, 'pagination', count=1)

    def test_index_query_one_keyword(self):
        '''
        Test index view with query of one keyword,
        which will display two products.
        '''

        products = [models.Product.active_objects.get(name='product_10')]
        response = self.client.get('/?query=10')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['products'],
            map(repr, products),
        )
        self.assertNotContains(response, 'pagination')

    def test_index_query_two_keywords(self):
        '''
        Test index view with query of two keywords,
        which will display three products.
        '''

        products = [
            models.Product.active_objects.get(name='product_2'),
            models.Product.active_objects.get(name='product_12'),
            models.Product.active_objects.get(name='product_9'),
        ]
        response = self.client.get('/?query=2 9')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['products'],
            map(repr, products),
            ordered=False,
        )
        self.assertNotContains(response, 'pagination')

    def test_index_query_no_result(self):
        '''
        Test index view with query of one keyword,
        which will display zero products.
        '''

        products = []
        response = self.client.get('/?query=product_0')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['products'],
            map(repr, products),
        )
        self.assertContains(response, 'No products found!')
        self.assertNotContains(response, 'pagination')

    def test_index_page_two(self):
        '''
        Test index view on page two.
        '''

        products = models.Product.active_objects.all()[self.page_len:]
        response = self.client.get('/2/')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['products'],
            map(repr, products),
        )
        self.assertContains(response, 'pagination', count=1)

    def test_index_404(self):
        '''
        Test index view on page three, which should return a 404 error.
        '''

        response = self.client.get('/3/')
        self.assertEqual(response.status_code, 404)

    def test_index_page_two_query_one_keyword(self):
        '''
        Test index view on page two with query of one keyword.
        '''

        products = models.Product.active_objects.all()[12:]
        response = self.client.get('/2/?query=product')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['products'],
            map(repr, products),
        )
        self.assertContains(response, 'pagination', count=1)

    ### Product Details Tests ###
    def test_details(self):
        '''
        Test details view with active product.
        '''

        product = models.Product.active_objects.get(pk=1)
        response = self.client.get('/commerce/product/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], product)

    def test_details_discontinued(self):
        '''
        Test details view with discontinued product.
        '''

        product = models.Product.objects.get(pk=15)
        response = self.client.get('/commerce/product/15/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], product)
        self.assertNotContains(response, 'Add')

    def test_details_404_invalid_pk(self):
        '''
        Test details view with nonexistent product,
        which should return a 404 error.
        '''

        response = self.client.get('/commerce/product/100/')
        self.assertEqual(response.status_code, 404)

    def test_details_out_of_stock(self):
        '''
        Test details view with out-of-stock product.
        '''

        product = models.Product.objects.get(pk=3)
        response = self.client.get('/commerce/product/3/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], product)
        self.assertNotContains(response, 'Add')

    ### Add Product Tests ###
    def test_add_product(self):
        '''
        Test add_product view with active product.
        '''

        response = self.client.get('/commerce/add_product/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 1)

    def test_add_product_next(self):
        '''
        Test add_product view with active product and next query.
        '''

        url = '/commerce/product/1/'
        response = self.client.get('/commerce/add_product/1/?next=' + url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, url)

        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 1)

    def test_add_product_discontinued(self):
        '''
        Test add_product view with discontinued product.
        '''

        response = self.client.get('/commerce/add_product/15/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        cart = self.client.session.get('cart', None)
        self.assertIs(cart, None)

    def test_add_product_invalid_pk(self):
        '''
        Test add_product view with nonexistent product.
        '''

        response = self.client.get('/commerce/add_product/100/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        cart = self.client.session.get('cart', None)
        self.assertIs(cart, None)

    def test_add_product_out_of_stock(self):
        '''
        Test add_product view with out-of-stock product.
        '''

        response = self.client.get('/commerce/add_product/3/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        cart = self.client.session.get('cart', None)
        self.assertIs(cart, None)

    def test_add_product_over_stock(self):
        '''
        Test add_product view with in-stock product,
        but try to add one more than stock.
        add_product should gracefully fail.
        '''

        session = self.client.session
        session['cart'] = {'2': 3}
        session.save()

        response = self.client.get('/commerce/add_product/2/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        cart = self.client.session['cart']
        self.assertEqual(cart['2'], 3)

    ### Delete Product Tests ###
    def test_delete_product_with_cart(self):
        '''
        Test delete_product view with cart.
        '''

        session = self.client.session
        session['cart'] = {'1': 3}
        session.save()

        response = self.client.get('/commerce/delete_product/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        cart = self.client.session['cart']
        self.assertEqual(cart, {})

    def test_delete_product_with_cart_next(self):
        '''
        Test delete_product view with cart and next query.
        '''

        session = self.client.session
        session['cart'] = {'1': 3}
        session.save()

        url = '/commerce/cart/'
        response = self.client.get('/commerce/delete_product/1/?next=' + url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, url)

        cart = self.client.session['cart']
        self.assertEqual(cart, {})

    def test_delete_product_not_in_cart(self):
        '''
        Test delete_product view with active product not in cart.
        '''

        response = self.client.get('/commerce/delete_product/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        cart = self.client.session['cart']
        self.assertEqual(cart, {})

    ### Cart Tests ###
    def test_cart(self):
        '''
        Test cart view with cart using GET.
        '''

        session = self.client.session
        session['cart'] = {'1': 3, '5': 2}
        session.save()

        response = self.client.get('/commerce/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
        self.assertContains(response, 'value="3"', count=1)
        self.assertContains(response, 'value="2"', count=1)

    def test_cart_empty_get(self):
        '''
        Test cart view with empty cart using GET.
        '''

        response = self.client.get('/commerce/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'form')
        self.assertContains(response, 'Cart is empty.', count=1)

    def test_cart_empty_post_checkout(self):
        '''
        Test cart view with empty cart using POST data
        submitted through checkout button.
        '''

        response = self.client.post(
            '/commerce/cart/',
            {'1': 3, 'five': 'two', 'checkout': 'Checkout'},
        )
        self.assertEqual(response.status_code, 200)

        cart = self.client.session['cart']
        self.assertEqual(cart, {})

        self.assertContains(response, 'Cart is empty.', count=1)

    def test_cart_empty_post_update(self):
        '''
        Test cart view with empty cart using POST data
        submitted through update button.
        '''

        response = self.client.post('/commerce/cart/', {'1': 3, 'five': 'two'})
        self.assertEqual(response.status_code, 200)

        cart = self.client.session['cart']
        self.assertEqual(cart, {})

        self.assertContains(response, 'Cart is empty.', count=1)

    def test_cart_post_checkout_no_update(self):
        '''
        Test cart view with cart using no POST data
        submitted through checkout button.
        '''

        session = self.client.session
        session['cart'] = {'1': 3, '5': 2}
        session.save()

        response = self.client.post('/commerce/cart/', {'checkout': 'Checkout'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/commerce/checkout/')

        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 3)
        self.assertEqual(cart['5'], 2)

    def test_cart_post_checkout_with_update(self):
        '''
        Test cart view with cart using POST data
        submitted through checkout button.
        '''

        session = self.client.session
        session['cart'] = {'1': 3, '5': 2}
        session.save()

        response = self.client.post(
            '/commerce/cart/',
            {'1': 2, 'checkout': 'Checkout'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/commerce/checkout/')

        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 2)
        self.assertEqual(cart['5'], 2)

    def test_cart_post_checkout_with_invalid_update(self):
        '''
        Test cart view with cart using invalid POST data
        submitted through checkout button.
        '''

        session = self.client.session
        session['cart'] = {'1': 3, '5': 2}
        session.save()

        response = self.client.post(
            '/commerce/cart/',
            {'1': 2, 'five': 'three', 'checkout': 'Checkout'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/commerce/checkout/')

        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 2)
        self.assertEqual(cart['5'], 2)

    def test_cart_post_update_no_update(self):
        '''
        Test cart view with cart using no POST data
        submitted through update button.
        '''

        session = self.client.session
        session['cart'] = {'1': 3, '5': 2}
        session.save()

        response = self.client.post('/commerce/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="3"', count=1)
        self.assertContains(response, 'value="2"', count=1)

        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 3)
        self.assertEqual(cart['5'], 2)

    def test_cart_post_update_with_update(self):
        '''
        Test cart view with cart using POST data
        submitted through update button.
        '''

        session = self.client.session
        session['cart'] = {'1': 3, '5': 2}
        session.save()

        response = self.client.post(
            '/commerce/cart/',
            {'1': 2},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="2"', count=2)

        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 2)
        self.assertEqual(cart['5'], 2)

    def test_cart_post_update_with_invalid_update(self):
        '''
        Test cart view with cart using invalid POST data
        submitted through update button.
        '''

        session = self.client.session
        session['cart'] = {'1': 3, '5': 2}
        session.save()

        response = self.client.post(
            '/commerce/cart/',
            {'1': 2, 'five': 'three'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
        self.assertContains(response, 'value="2"', count=2)

        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 2)
        self.assertEqual(cart['5'], 2)

    def test_cart_post_update_with_over_stock_update(self):
        '''
        Test cart view with cart using POST data that goes over stock limit
        submitted through update button.
        '''

        session = self.client.session
        session['cart'] = {'2': 1}
        session.save()

        response = self.client.post('/commerce/cart/', {'2': 4})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
        self.assertContains(response, 'value="3"', count=1)

        cart = self.client.session['cart']
        self.assertEqual(cart['2'], 3)

    def test_cart_post_checkout_with_over_stock_update(self):
        '''
        Test cart view with cart using POST data that goes over stock limit
        submitted through checkout button.
        '''

        session = self.client.session
        session['cart'] = {'2': 1}
        session.save()

        response = self.client.post(
            '/commerce/cart/',
            {'2': 4, 'checkout': 'Checkout'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/commerce/checkout/')

        cart = self.client.session['cart']
        self.assertEqual(cart['2'], 3)

    def test_cart_get_with_invalid_cart(self):
        '''
        Test cart view with invalid cart using GET.
        '''

        session = self.client.session
        session['cart'] = {'3': 1, '15': 1}
        session.save()

        response = self.client.get('/commerce/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'form')
        self.assertContains(response, 'error list', count=1)
        self.assertContains(response, 'Cart is empty.', count=1)

        cart = self.client.session['cart']
        self.assertEqual(cart, {})

    def test_cart_post_update_with_invalid_cart(self):
        '''
        Test cart view with invalid cart using no POST data
        submitted through update button.
        '''

        session = self.client.session
        session['cart'] = {'3': 1, '15': 1}
        session.save()

        response = self.client.post('/commerce/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'form')
        self.assertContains(response, 'error list', count=1)
        self.assertContains(response, 'Cart is empty.', count=1)

        cart = self.client.session['cart']
        self.assertEqual(cart, {})

    def test_cart_post_checkout_with_invalid_cart(self):
        '''
        Test cart view with invalid cart using no POST data
        submitted through checkout button.
        '''

        session = self.client.session
        session['cart'] = {'3': 1, '15': 1}
        session.save()

        response = self.client.post('/commerce/cart/', {'checkout': 'Checkout'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'form')
        self.assertContains(response, 'error list', count=1)
        self.assertContains(response, 'Cart is empty.', count=1)

        cart = self.client.session['cart']
        self.assertEqual(cart, {})

    ### Checkout Tests ###
    def test_checkout_no_login_no_cart_no_address_no_card(self):
        '''
        Test checkout view with no login, no cart, no address, and no card using GET,
        which should return a redirect response.
        '''

        url = '/commerce/checkout/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/login/?next=' + url)

    def test_checkout_login_no_cart_no_address_no_card(self):
        '''
        Test checkout view with login, no cart, no address, and no card using GET,
        which should return a redirect response.
        '''

        user = User.objects.get(username='user_1')
        self.client.force_login(user)

        response = self.client.get('/commerce/checkout/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        cart = self.client.session['cart']
        self.assertEqual(cart, {})

    def test_checkout_login_cart_no_address_no_card(self):
        '''
        Test checkout view with login, cart, no address, and no card using GET,
        which should return a redirect response.
        '''

        user = User.objects.get(username='user_1')
        self.client.force_login(user)

        session = self.client.session
        session['cart'] = temp_cart = {'1': 2}
        session.save()

        url = '/commerce/checkout/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/addresses/add_address/?next=' + url)

        cart = self.client.session['cart']
        self.assertEqual(cart, temp_cart)

    def test_checkout_login_cart_address_no_card(self):
        '''
        Test checkout view with login, cart, address, and no card using GET,
        which should return a redirect response.
        '''

        user = User.objects.get(username='user_3')
        self.client.force_login(user)

        session = self.client.session
        session['cart'] = temp_cart = {'1': 2}
        session.save()

        url = '/commerce/checkout/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/cards/add_card/?next=' + url)

        cart = self.client.session['cart']
        self.assertEqual(cart, temp_cart)

    def test_checkout_get(self):
        '''
        Test checkout view using GET.
        '''

        user = User.objects.get(username='user_2')
        self.client.force_login(user)

        session = self.client.session
        session['cart'] = temp_cart = {'1': 2}
        session.save()

        response = self.client.get('/commerce/checkout/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertContains(response, 'type="radio"', count=2)

        cart = self.client.session['cart']
        self.assertEqual(cart, temp_cart)

    def test_checkout_get_with_invalid_cart(self):
        '''
        Test checkout with invalid cart using GET.
        '''

        user = User.objects.get(username='user_2')
        self.client.force_login(user)

        session = self.client.session
        session['cart'] = {'3': 1, '15': 1}
        session.save()

        response = self.client.get('/commerce/checkout/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('form', response.context)
        self.assertContains(response, 'error list', count=1)
        self.assertContains(response, 'Cart is empty.', count=1)

        cart = self.client.session['cart']
        self.assertEqual(cart, {})

    def test_checkout_post_with_invalid_cart(self):
        '''
        Test checkout with invalid cart using POST data.
        '''

        user = User.objects.get(username='user_2')
        self.client.force_login(user)

        session = self.client.session
        session['cart'] = {'3': 1, '15': 1}
        session.save()

        response = self.client.post(
            '/commerce/checkout/',
            {
                'cvv': 210,
                'address': 1,
                'card': 1,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('form', response.context)
        self.assertContains(response, 'error list', count=1)
        self.assertContains(response, 'Cart is empty.', count=1)

        cart = self.client.session['cart']
        self.assertEqual(cart, {})

    def test_checkout_post_with_partly_invalid_cart(self):
        '''
        Test checkout with invalid cart using POST data.
        '''

        user = User.objects.get(username='user_2')
        self.client.force_login(user)

        session = self.client.session
        session['cart'] = {'3': 1, '1': 2}
        session.save()

        response = self.client.post(
            '/commerce/checkout/',
            {
                'cvv': 210,
                'address': 1,
                'card': 1,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertContains(response, 'type="radio"', count=2)
        self.assertContains(response, 'error list', count=1)
        self.assertContains(response, 'value="210"', count=1)

        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 2)

    def test_checkout_invalid_post_with_cart(self):
        '''
        Test checkout with cart using invalid POST data.
        '''

        user = User.objects.get(username='user_2')
        self.client.force_login(user)

        session = self.client.session
        session['cart'] = {'1': 2, '5': 3}
        session.save()

        response = self.client.post(
            '/commerce/checkout/',
            {
                'cvv': 210,
                'address': 2,
                'card': 3,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertContains(response, 'type="radio"', count=2)
        self.assertContains(response, 'error list', count=2)
        self.assertContains(response, 'value="210"', count=1)

        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 2)
        self.assertEqual(cart['5'], 3)

    def test_checkout_post_with_cart(self):
        '''
        Test checkout with cart using POST data.
        '''

        user = User.objects.get(username='user_2')
        self.client.force_login(user)

        session = self.client.session
        session['cart'] = {'1': 2, '5': 3}
        session.save()

        response = self.client.post(
            '/commerce/checkout/',
            {
                'cvv': 210,
                'address': 1,
                'card': 1,
            },
        )
        self.assertEqual(response.status_code, 302)

        orders = user.orders.all()
        self.assertEqual(len(orders), 1)
        order = orders.first()
        self.assertEqual(order.total, Decimal('363.16'))
        self.assertEqual(response.url, '/commerce/thank_you/%d/' % order.pk)

        items = order.orderitem_set.all()
        self.assertEqual(len(items), 2)
        for item in items:
            if item.product.pk == 1:
                self.assertEqual(item.quantity, 2)
            elif item.product.pk == 5:
                self.assertEqual(item.quantity, 3)

        cart = self.client.session['cart']
        self.assertEqual(cart, {})

    ### Thank You Tests ###
    def test_thank_you_get(self):
        '''
        Test thank_you view using GET.
        '''

        user = User.objects.get(username='user_3')
        self.client.force_login(user)

        response = self.client.get('/commerce/thank_you/1/')
        self.assertEqual(response.status_code, 200)

        order = user.orders.first()
        self.assertEqual(response.context['order'], order)

    def test_thank_you_post(self):
        '''
        Test thank_you view using junk POST data.
        '''

        user = User.objects.get(username='user_3')
        self.client.force_login(user)

        response = self.client.post(
            '/commerce/thank_you/1/',
            {
                'data_1': 'junk_1',
                'data_2': 'junk_2',
            },
        )
        self.assertEqual(response.status_code, 200)

        order = user.orders.first()
        self.assertEqual(response.context['order'], order)

    def test_thank_you_get_invalid_pk(self):
        '''
        Test thank_you view using GET with invalid order pk.
        '''

        user = User.objects.get(username='user_3')
        self.client.force_login(user)

        response = self.client.get('/commerce/thank_you/2/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

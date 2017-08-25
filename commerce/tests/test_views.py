import datetime
from decimal import Decimal
from django.test import TestCase
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from .. import models

class NavTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='user_1',
            password='password_1',
        )
        user = User.objects.create_user(
            username='user_2',
            password='password_2',
            is_staff=True,
        )

    def test_no_login(self):
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

    def test_login(self):
        '''
        Test navigation bar with normal login session.
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

    def test_admin_login(self):
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

class IndexTestCase(TestCase):
    def setUp(self):
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
            4,
        ]

        self.page_len = 12

        for i in range(0, len(prices)):
            models.Product.objects.create(
                name='product_%d' % (i + 1),
                price=prices[i],
                description='',
                stock=stocks[i],
                image='product_%d.jpg' % (i + 1),
            )

        product = models.Product.objects.get(name='product_15')
        product.discontinued = True
        product.save()

    def test_no_query(self):
        '''
        Test index with no query.
        '''

        products = models.Product.active_objects.all()[:self.page_len]
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['products'], map(repr, products))
        self.assertContains(response, 'pagination', count=1)

    def test_query_one_keyword(self):
        '''
        Test index with one keyword query,
        which displays two products.
        '''

        products = [models.Product.active_objects.get(name='product_10')]
        response = self.client.get('/?query=10')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['products'],
            map(repr, products),
        )
        self.assertNotContains(response, 'pagination')

    def test_query_two_keywords(self):
        '''
        Test index with two keywords query,
        which displays three products.
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

    def test_query_no_result(self):
        '''
        Test index with one keyword query,
        which displays zero products.
        '''

        products = []
        response = self.client.get('/?query=product_15')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['products'],
            map(repr, products),
        )
        self.assertContains(response, 'No products found!')
        self.assertNotContains(response, 'pagination')

    def test_page_two(self):
        '''
        Test index on page two.
        '''

        products = models.Product.active_objects.all()[self.page_len:]
        response = self.client.get('/2/')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['products'],
            map(repr, products),
        )
        self.assertContains(response, 'pagination', count=1)

    def test_page_two_query_one_keyword(self):
        '''
        Test index on page two with one keyword query.
        '''

        products = models.Product.active_objects.all()[self.page_len:]
        response = self.client.get('/2/?query=product')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['products'],
            map(repr, products),
        )
        self.assertContains(response, 'pagination', count=1)

    def test_404(self):
        '''
        Test index on page three, which displays 404 error.
        '''

        response = self.client.get('/3/')
        self.assertEqual(response.status_code, 404)

class DetailsTestCase(TestCase):
    def setUp(self):
        models.Product.objects.create(
            pk=1,
            name='product_1',
            price='0.99',
            description='product_1 description',
            stock=5,
            image='product_1.jpg',
        )

        models.Product.objects.create(
            pk=2,
            name='product_2',
            price='0.99',
            description='',
            stock=5,
            image='product_2.jpg',
        )

        models.Product.objects.create(
            pk=3,
            name='product_3',
            price='0.99',
            description='',
            stock=5,
            image='product_3.jpg',
            discontinued=True,
        )

        models.Product.objects.create(
            pk=4,
            name='product_4',
            price='0.99',
            description='',
            stock=0,
            image='product_4.jpg',
        )

    def test_product(self):
        '''
        Test details with active product.
        '''

        product = models.Product.active_objects.get(pk=1)
        response = self.client.get('/commerce/product/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], product)
        self.assertContains(response, product.description, count=1)

    def test_product_no_description(self):
        '''
        Test details with active, nondescript product.
        '''

        product = models.Product.active_objects.get(pk=2)
        response = self.client.get('/commerce/product/2/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], product)
        self.assertContains(response, 'No Description', count=1)

    def test_product_discontinued(self):
        '''
        Test details with discontinued product.
        '''

        product = models.Product.objects.get(pk=3)
        response = self.client.get('/commerce/product/3/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], product)
        self.assertNotContains(response, 'Add')

    def test_product_out_of_stock(self):
        '''
        Test details with out-of-stock product.
        '''

        product = models.Product.objects.get(pk=4)
        response = self.client.get('/commerce/product/4/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], product)
        self.assertNotContains(response, 'Add')

    def test_invalid_pk(self):
        '''
        Test details with nonexistent product,
        which displays 404 error.
        '''

        response = self.client.get('/commerce/product/5/')
        self.assertEqual(response.status_code, 404)

class AddProductTestCase(TestCase):
    def setUp(self):
        models.Product.objects.create(
            pk=1,
            name='product_1',
            price='0.99',
            description='',
            stock=5,
            image='product_1.jpg',
        )

        models.Product.objects.create(
            pk=2,
            name='product_2',
            price='0.99',
            description='',
            stock=5,
            image='product_2.jpg',
            discontinued=True,
        )

        models.Product.objects.create(
            pk=3,
            name='product_3',
            price='0.99',
            description='',
            stock=0,
            image='product_3.jpg',
        )

    def test_product_no_cart(self):
        '''
        Test add_product with active product and no cart.
        '''

        response = self.client.get('/commerce/add_product/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 1)

    def test_product_cart(self):
        '''
        Test add_product with active product and cart.
        '''

        session = self.client.session
        session['cart'] = {'1': 3}
        session.save()

        response = self.client.get('/commerce/add_product/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 4)

    def test_product_next(self):
        '''
        Test add_product with active product and next variable.
        '''

        url = '/commerce/product/1/'
        response = self.client.get('/commerce/add_product/1/?next=' + url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, url)

        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 1)

    def test_product_discontinued(self):
        '''
        Test add_product with discontinued product.
        '''

        response = self.client.get('/commerce/add_product/2/')
        self.assertEqual(response.status_code, 404)

    def test_product_out_of_stock(self):
        '''
        Test add_product with out-of-stock product.
        '''

        response = self.client.get('/commerce/add_product/3/')
        self.assertEqual(response.status_code, 404)

    def test_product_over_stock(self):
        '''
        Test add_product with in-stock product,
        but try to add one more than stock.
        '''

        session = self.client.session
        session['cart'] = {'1': 5}
        session.save()

        response = self.client.get('/commerce/add_product/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 5)

    def test_product_nonexist_product(self):
        '''
        Test add_product with nonexistent product.
        '''

        response = self.client.get('/commerce/add_product/4/')
        self.assertEqual(response.status_code, 404)

    def test_product_nonnumeric_pk(self):
        '''
        Test add_product with nonnumeric primary key.
        '''

        response = self.client.get('/commerce/add_product/a/')
        self.assertEqual(response.status_code, 404)

class DeleteProductTestCase(TestCase):
    def setUp(self):
        models.Product.objects.create(
            pk=1,
            name='product_1',
            price='0.99',
            description='',
            stock=5,
            image='product_1.jpg',
        )

        models.Product.objects.create(
            pk=2,
            name='product_2',
            price='0.99',
            description='',
            stock=5,
            image='product_2.jpg',
            discontinued=True,
        )

        models.Product.objects.create(
            pk=3,
            name='product_3',
            price='0.99',
            description='',
            stock=0,
            image='product_3.jpg',
        )

    def test_product_with_cart(self):
        '''
        Test delete_product with active product and cart.
        '''

        session = self.client.session
        session['cart'] = {'1': 3}
        session.save()

        response = self.client.get('/commerce/delete_product/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        cart = self.client.session['cart']
        self.assertEqual(cart, {})

    def test_product_no_cart(self):
        '''
        Test delete_product with active product and no cart.
        '''

        response = self.client.get('/commerce/delete_product/1/')
        self.assertEqual(response.status_code, 404)

    def test_product_next(self):
        '''
        Test delete_product with next variable.
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

    def test_product_not_in_cart(self):
        '''
        Test delete_product with product not in cart.
        '''

        session = self.client.session
        session['cart'] = {'2': 1}
        session.save()

        response = self.client.get('/commerce/delete_product/1/')
        self.assertEqual(response.status_code, 404)

        cart = self.client.session['cart']
        self.assertEqual(cart, {'2': 1})

    def test_nonnumeric_pk(self):
        '''
        Test delete_product with nonnumeric primary key.
        '''

        response = self.client.get('/commerce/delete_product/a/')
        self.assertEqual(response.status_code, 404)

class CartTestCase(TestCase):
    def setUp(self):
        models.Product.objects.create(
            pk=1,
            name='product_1',
            price='0.99',
            description='',
            stock=5,
            image='product_1.jpg',
        )

        models.Product.objects.create(
            pk=2,
            name='product_2',
            price='0.99',
            description='',
            stock=3,
            image='product_2.jpg',
        )

        models.Product.objects.create(
            pk=3,
            name='product_3',
            price='0.99',
            description='',
            stock=5,
            image='product_3.jpg',
            discontinued=True,
        )

        models.Product.objects.create(
            pk=4,
            name='product_4',
            price='0.99',
            description='',
            stock=0,
            image='product_4.jpg',
        )

    def test_cart_with_one_product(self):
        '''
        Test cart with one product.
        '''

        session = self.client.session
        session['cart'] = {'1': 3}
        session.save()

        response = self.client.get('/commerce/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="3"', count=1)

    def test_cart_with_two_products(self):
        '''
        Test cart with two products.
        '''

        session = self.client.session
        session['cart'] = {'1': 3, '2': 1}
        session.save()

        response = self.client.get('/commerce/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="3"', count=1)
        self.assertContains(response, 'value="1"', count=1)

    def test_empty_cart(self):
        '''
        Test empty cart.
        '''

        response = self.client.get('/commmerce/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cart is empty.', count=1)

    def test_empty_cart_valid_checkout(self):
        '''
        Test empty cart with valid data submitted using checkout.
        '''

        response = self.client.post(
            '/commerce/cart/',
            {'1': 3, '2': 1, 'checkout': ''},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/commerce/cart/')
        cart = self.client.session['cart']
        self.assertEqual(cart, {})

    def test_empty_cart_invalid_checkout(self):
        '''
        Test empty cart with invalid data submitted using checkout.
        '''

        response = self.client.post(
            '/commerce/cart/',
            {'abc': 123, 'checkout': ''},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/commerce/cart/')
        cart = self.client.session['cart']
        self.assertEqual(cart, {})

    def test_empty_cart_empty_checkout(self):
        '''
        Test empty cart with empty data submitted using checkout.
        '''

        response = self.client.post(
            '/commerce/cart/',
            {'checkout': ''},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/commerce/cart/')
        cart = self.client.session['cart']
        self.assertEqual(cart, {})

    def test_empty_cart_valid_update(self):
        '''
        Test empty cart with valid data submitted using update.
        '''

        response = self.client.post(
            '/commerce/cart/',
            {'1': 3, '2': 1},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/commerce/cart/')
        cart = self.client.session['cart']
        self.assertEqual(cart, {})

    def test_empty_cart_invalid_update(self):
        '''
        Test empty cart with invalid data submitted using update.
        '''

        response = self.client.post(
            '/commerce/cart/',
            {'abc': 123},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/commerce/cart/')
        cart = self.client.session['cart']
        self.assertEqual(cart, {})

    def test_empty_cart_empty_update(self):
        '''
        Test empty cart with empty data submitted using update.
        '''

        response = self.client.post('/commerce/cart/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/commerce/cart/')
        cart = self.client.session['cart']
        self.assertEqual(cart, {})

    def test_cart_valid_checkout(self):
        '''
        Test cart with valid data submitted using checkout.
        '''

        session = self.client.session
        session['cart'] = {'1': 2, '2': 1}
        session.save()

        response = self.client.post(
            '/commerce/cart/',
            {'1': 3, '2': 1, 'checkout': ''}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/commerce/checkout/')

        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 3)
        self.assertEqual(cart['2'], 1)

    def test_cart_invalid_checkout(self):
        '''
        Test cart with invalid data submitted using checkout.
        '''

        session = self.client.session
        session['cart'] = {'1': 2, '2': 1}
        session.save()

        response = self.client.post(
            '/commerce/cart/',
            {'abc': 123, 'checkout': ''},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/commerce/cart/')

        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 2)
        self.assertEqual(cart['2'], 1)

    def test_cart_empty_checkout(self):
        '''
        Test cart with empty data submitted using checkout.
        '''

        session = self.client.session
        session['cart'] = {'1': 2, '2': 1}
        session.save()

        response = self.client.post(
            '/commerce/cart/',
            {'checkout': ''},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/commerce/cart/')

        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 2)
        self.assertEqual(cart['2'], 1)

    def test_cart_valid_update(self):
        '''
        Test cart with valid data submitted using update.
        '''

        session = self.client.session
        session['cart'] = {'1': 2, '2': 1}
        session.save()

        response = self.client.post(
            '/commerce/cart/',
            {'1': 3, '2': 1},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/commerce/cart/')

        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 3)
        self.assertEqual(cart['2'], 1)

    def test_cart_invalid_update(self):
        '''
        Test cart with invalid data submitted using update.
        '''

        session = self.client.session
        session['cart'] = {'1': 2, '2': 1}
        session.save()

        response = self.client.post(
            '/commerce/cart/',
            {'abc': 123},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/commerce/cart/')
        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 2)
        self.assertEqual(cart['2'], 1)

    def test_cart_empty_update(self):
        '''
        Test cart with empty data submitted using update.
        '''

        session = self.client.session
        session['cart'] = {'1': 2, '2': 1}
        session.save()

        url = '/commerce/cart/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, url)
        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 2)
        self.assertEqual(cart['2'], 1)

    def test_cart_valid_update_exceed_stock(self):
        '''
        Test cart with valid data, exceeding stock, submitted using update.
        '''

        session = self.client.session
        session['cart'] = {'2': 1}
        session.save()

        url = '/commerce/cart/'
        response = self.client.post(url, {'2': 4})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, url)

        cart = self.client.session['cart']
        self.assertEqual(cart['2'], 3)

    def test_cart_valid_checkout_exceed_stock(self):
        '''
        Test cart with valid data, exceeding stock, submitted using checkout.
        '''

        session = self.client.session
        session['cart'] = {'2': 1}
        session.save()

        url = '/commerce/checkout/'
        response = self.client.post(
            url,
            {'2': 4, 'checkout': ''},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, url)

        cart = self.client.session['cart']
        self.assertEqual(cart['2'], 3)

    def test_cart_discontinued_product(self):
        '''
        Test cart with discontinued product.
        '''

        session = self.client.session
        session['cart'] = {'3': 1}
        session.save()

        response = self.client.get('/commerce/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'form')
        self.assertContains(response, 'error list', count=1)
        self.assertContains(response, 'Cart is empty.', count=1)

        cart = self.client.session['cart']
        self.assertEqual(cart, {})

    def test_cart_out_of_stock_product(self):
        '''
        Test cart with out-of-stock product.
        '''

        session = self.client.session
        session['cart'] = {'4': 1}
        session.save()

        response = self.client.post('/commerce/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'form')
        self.assertContains(response, 'error list', count=1)
        self.assertContains(response, 'Cart is empty.', count=1)

        cart = self.client.session['cart']
        self.assertEqual(cart, {})

    def test_cart_nonexist_product(self):
        '''
        Test cart with nonexistent product.
        '''

        session = self.client.session
        session['cart'] = {'5': 1}
        session.save()

        response = self.client.get('/commerce/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'form')
        self.assertContains(response, 'error list', count=1)
        self.assertContains(response, 'Cart is empty.', count=1)

        cart = self.client.session['cart']
        self.assertEqual(cart, {})

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
            number='',
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

    ### Cart Tests ###

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

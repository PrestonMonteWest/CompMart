import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from commerce import models

class TestViews(TestCase):
    def setUp(self):
        product_1 = models.Product.objects.create(
            name='product_1',
            price='1.99',
            description='',
            stock=5,
            image='product_1.jpg',
        )

        product_2 = models.Product.objects.create(
            name='product_2',
            price='1.99',
            description='',
            stock=5,
            image='product_2.jpg',
        )

        User.objects.create_user(
            username='user_1',
            first_name='name_1',
            password='password_1',
        )

        user = User.objects.create_user(
            username='user_2',
            first_name='name_2',
            password='password_2',
        )
        user.addresses.create(
            pk=1,
            street='street_1',
            city='city_1',
            state='S1',
            zip_code='zip_1',
        )

        user = User.objects.create_user(
            username='user_3',
            first_name='name_3',
            password='password_3',
        )
        user.addresses.create(
            pk=2,
            street='street_2',
            city='city_2',
            state='S2',
            zip_code='zip_2',
        )
        user.cards.create(
            pk=1,
            card_number='',
            card_type='type_1',
            holder_name='name_1',
            expiration_date=datetime.date.today(),
        )

        user = User.objects.create_user(
            username='user_4',
            first_name='name_4',
            password='password_4',
        )
        address = user.addresses.create(
            pk=3,
            street='street_3',
            city='city_3',
            state='S3',
            zip_code='zip_3',
        )
        card = user.cards.create(
            pk=2,
            card_number='',
            card_type='type_2',
            holder_name='name_2',
            expiration_date=datetime.date.today(),
        )
        order = user.orders.create(
            pk=1,
            card=card,
            street=address.street,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
            total='1.99',
        )
        models.OrderItem.objects.create(
            pk=1,
            order=order,
            product=product_1,
            purchase_price='1.99',
            quantity=1,
        )

        user = User.objects.create_user(
            username='user_5',
            first_name='name_5',
            password='password_5',
        )
        address = user.addresses.create(
            pk=4,
            street='street_4',
            city='city_4',
            state='S4',
            zip_code='zip_4',
        )
        card = user.cards.create(
            pk=3,
            card_number='',
            card_type='type_3',
            holder_name='name_3',
            expiration_date=datetime.date.today(),
        )
        order = user.orders.create(
            pk=2,
            card=card,
            street=address.street,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
            total='1.99',
        )
        models.OrderItem.objects.create(
            pk=2,
            order=order,
            product=product_1,
            purchase_price='1.99',
            quantity=1,
        )
        models.Review.objects.create(
            pk=1,
            product=product_1,
            user=user,
            title='title_1',
            body='body_1',
            rating=50,
        )

        user = User.objects.create_user(
            username='user_6',
            first_name='name_6',
            password='password_6',
        )
        user.addresses.create(
            pk=5,
            street='street_5',
            city='city_5',
            state='S5',
            zip_code='zip_5',
        )
        address = user.addresses.create(
            pk=6,
            street='street_6',
            city='city_6',
            state='S6',
            zip_code='zip_6',
        )
        user.cards.create(
            pk=4,
            card_number='',
            card_type='type_4',
            holder_name='name_4',
            expiration_date=datetime.date.today(),
        )
        card = user.cards.create(
            pk=5,
            card_number='',
            card_type='type_5',
            holder_name='name_5',
            expiration_date=datetime.date.today(),
        )
        order = user.orders.create(
            pk=3,
            card=card,
            street=address.street,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
            total='1.99',
        )
        models.OrderItem.objects.create(
            pk=3,
            order=order,
            product=product_1,
            purchase_price='1.99',
            quantity=1,
        )
        order = user.orders.create(
            pk=4,
            card=card,
            street=address.street,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
            total='1.99',
        )
        models.OrderItem.objects.create(
            pk=4,
            order=order,
            product=product_2,
            purchase_price='1.99',
            quantity=1,
        )
        models.Review.objects.create(
            pk=2,
            product=product_1,
            user=user,
            title='title_2',
            body='body_2',
            rating=50,
        )
        models.Review.objects.create(
            pk=3,
            product=product_2,
            user=user,
            title='title_3',
            body='body_3',
            rating=50,
        )

    def test_index_no_address_no_card_no_order_no_review(self):
        user = User.objects.get(username='user_1')
        self.client.force_login(user)

        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add Address', count=1)
        self.assertContains(response, 'Add Card', count=1)
        self.assertNotContains(response, 'Orders')
        self.assertNotContains(response, 'Reviews')

    def test_index_no_card_no_order_no_review(self):
        user = User.objects.get(username='user_2')
        self.client.force_login(user)

        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Addresses', count=1)
        self.assertContains(response, 'Add Card', count=1)
        self.assertNotContains(response, 'Orders')
        self.assertNotContains(response, 'Reviews')

    def test_index_no_order_no_review(self):
        user = User.objects.get(username='user_3')
        self.client.force_login(user)

        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Addresses', count=1)
        self.assertContains(response, 'Cards', count=1)
        self.assertNotContains(response, 'Orders')
        self.assertNotContains(response, 'Reviews')

    def test_index_no_review(self):
        user = User.objects.get(username='user_4')
        self.client.force_login(user)

        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Addresses', count=1)
        self.assertContains(response, 'Cards', count=1)
        self.assertContains(response, 'Orders', count=1)
        self.assertNotContains(response, 'Reviews')

    def test_index(self):
        '''
        Test index with login and instances of all related models.
        '''

        user = User.objects.get(username='user_5')
        self.client.force_login(user)

        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Addresses', count=1)
        self.assertContains(response, 'Cards', count=1)
        self.assertContains(response, 'Orders', count=1)
        self.assertContains(response, 'Reviews', count=1)

    def test_index_no_login(self):
        '''
        Test index with no login.
        '''

        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/login/?next=/account/')

    def test_register(self):
        '''
        Test register using GET.
        '''

        response = self.client.get('/account/register/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

    def test_register_login(self):
        '''
        Test register with login using GET.
        '''

        user = User.objects.get(username='user_1')
        self.client.force_login(user)

        response = self.client.get('/account/register/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

    def test_register_post(self):
        '''
        Test register using POST data.
        '''

        response = self.client.post(
            '/account/register/',
            {
                'username': 'user_7',
                'first_name': 'name_7',
                'password1': 'password_7',
                'password2': 'password_7',
                'email': 'user_7@example.com',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        # test email verification

        user = User.objects.get(username='user_7')
        self.assertEqual(user.first_name, 'name_7')
        self.assertTrue(user.check_password('password_7'))
        self.assertEqual(user.email, 'user_7@example.com')

    def test_register_invalid_post(self):
        '''
        Test register using invalid POST data.
        '''

        response = self.client.post(
            '/account/register/',
            {
                'username': '!@#$%^&*()',
                'first_name': 'name_7',
                'password0': 'password_7',
                'password1': 'password_7',
                'email': '!@#$%^&*()_at_example.com',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'error list')

        self.assertIn('form', response.context)
        errors = response.context['form'].errors
        self.assertEqual(len(errors), 3)

    def test_login(self):
        '''
        Test login using GET.
        '''

        response = self.client.get('/account/login/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_login_with_login(self):
        '''
        Test login with login using GET.
        '''

        user = User.objects.get(username='user_1')
        self.client.force_login(user)

        response = self.client.get('/account/login/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_login_post(self):
        '''
        Test login using POST data.
        '''

        response = self.client.post(
            '/account/login/',
            {
                'username': 'user_1',
                'password': 'password_1',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        user = get_user(self.client)
        self.assertEqual(user.username, 'user_1')
        self.assertEqual(user.first_name, 'name_1')
        self.assertTrue(user.check_password('password_1'))

    def test_login_post_with_login(self):
        '''
        Test login with login using POST data.
        '''

        user = User.objects.get(username='user_2')
        self.client.force_login(user)

        response = self.client.post(
            '/account/login/',
            {
                'username': 'user_1',
                'password': 'password_1',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        user = get_user(self.client)
        self.assertEqual(user.username, 'user_1')
        self.assertEqual(user.first_name, 'name_1')
        self.assertTrue(user.check_password('password_1'))

    def test_login_post_with_next(self):
        '''
        Test login with next query parameter using POST data.
        '''

        response = self.client.post(
            '/account/login/?next=/account/',
            {
                'username': 'user_1',
                'password': 'password_1',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/')

        user = get_user(self.client)
        self.assertEqual(user.username, 'user_1')
        self.assertEqual(user.first_name, 'name_1')
        self.assertTrue(user.check_password('password_1'))

    def test_login_invalid_post(self):
        '''
        Test login using invalid POST data.
        '''

        response = self.client.post(
            '/account/login/',
            {
                'username': 'user_2',
                'password': 'password_1',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

        errors = response.context['form'].errors
        self.assertEqual(len(errors), 1)

    def test_logout(self):
        '''
        Test logout with login using GET.
        '''

        user = User.objects.get(username='user_1')
        self.client.force_login(user)

        response = self.client.get('/account/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        user = get_user(self.client)
        self.assertTrue(user.is_anonymous)

    def test_logout_no_login(self):
        '''
        Test logout with no login using GET.
        '''

        response = self.client.get('/account/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_logout_with_next(self):
        '''
        Test logout with login and next query parameter using GET.
        '''

        user = User.objects.get(username='user_1')
        self.client.force_login(user)

        response = self.client.get('/account/logout/?next=/commerce/cart/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/commerce/cart/')

        user = get_user(self.client)
        self.assertTrue(user.is_anonymous)

    def test_logout_with_cart(self):
        '''
        Test logout with login and cart using GET.
        '''

        user = User.objects.get(username='user_1')
        self.client.force_login(user)

        session = self.client.session
        session['cart'] = {'1': 3}
        session.save()

        response = self.client.get('/account/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        user = get_user(self.client)
        self.assertTrue(user.is_anonymous)

        self.assertIn('cart', self.client.session)
        cart = self.client.session['cart']
        self.assertEqual(cart['1'], 3)

    def test_address_list(self):
        pass

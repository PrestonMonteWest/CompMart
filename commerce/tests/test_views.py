from django.test import TestCase, Client
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from .. import models

class IndexTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='user_1',
            password='password_1',
        )
        User.objects.create_user(
            username='user_2',
            password='password_2',
            is_staff=True,
        )

        for i in range(1, 17):
            models.Product.objects.create(
                name='product_%d' % i,
                price='%d.99' % i,
                description='',
                stock=i,
                image='product_%d.jpg' % i,
            )

        site = Site.objects.get(pk=2)
        site.domain = 'localhost'
        site.name = 'CompMart'
        site.save()

        self.client = Client()

    def test_index(self):
        '''
        Test index view with no login and no query.
        '''

        products = models.Product.active_objects.all()[:12]
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['products'], map(repr, products))
        self.assertContains(response, 'Home', count=1)
        self.assertContains(response, 'Cart', count=1)
        self.assertContains(response, 'Login', count=1)
        self.assertContains(response, 'Register', count=1)
        self.assertNotContains(response, 'Logout')
        self.assertNotContains(response, 'Account')
        self.assertNotContains(response, 'Admin')

    def test_index_login(self):
        '''
        Test index view login of non-admin account and no query.
        '''

        products = models.Product.active_objects.all()[:12]
        user_1 = User.objects.get(username='user_1')

        self.client.force_login(user_1)
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['products'], map(repr, products))
        self.assertContains(response, 'Home', count=1)
        self.assertContains(response, 'Cart', count=1)
        self.assertNotContains(response, 'Login')
        self.assertNotContains(response, 'Register')
        self.assertContains(response, 'Logout', count=1)
        self.assertContains(response, 'Account', count=1)
        self.assertNotContains(response, 'Admin')

    def test_index_login_admin(self):
        '''
        Test index view with login of admin account and no query.
        '''

        products = models.Product.active_objects.all()[:12]
        user_2 = User.objects.get(username='user_2')

        self.client.force_login(user_2)
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['products'], map(repr, products))
        self.assertContains(response, 'Home', count=1)
        self.assertContains(response, 'Cart', count=1)
        self.assertNotContains(response, 'Login')
        self.assertNotContains(response, 'Register')
        self.assertContains(response, 'Logout', count=1)
        self.assertContains(response, 'Account', count=1)
        self.assertContains(response, 'Admin', count=1)

    def test_index_query_one_keyword(self):
        '''
        Test index view by querying one keyword,
        which will display two products.
        '''

        products = [models.Product.active_objects.get(name='product_10')]
        response = self.client.get('/?query=10')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['products'],
            map(repr, products),
        )
        self.assertContains(response, 'Home', count=1)
        self.assertContains(response, 'Cart', count=1)
        self.assertContains(response, 'Login', count=1)
        self.assertContains(response, 'Register', count=1)
        self.assertNotContains(response, 'Logout')
        self.assertNotContains(response, 'Account')
        self.assertNotContains(response, 'Admin')

    def test_index_query_two_keywords(self):
        '''
        Test index view by querying two keywords,
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
        self.assertContains(response, 'Home', count=1)
        self.assertContains(response, 'Cart', count=1)
        self.assertContains(response, 'Login', count=1)
        self.assertContains(response, 'Register', count=1)
        self.assertNotContains(response, 'Logout')
        self.assertNotContains(response, 'Account')
        self.assertNotContains(response, 'Admin')

    def test_index_query_no_result(self):
        '''
        Test index view by querying one keyword,
        which will display zero products.
        '''

        products = []
        response = self.client.get('/?query=product_0')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['products'],
            map(repr, products),
        )
        self.assertContains(response, 'Home', count=1)
        self.assertContains(response, 'Cart', count=1)
        self.assertContains(response, 'Login', count=1)
        self.assertContains(response, 'Register', count=1)
        self.assertNotContains(response, 'Logout')
        self.assertNotContains(response, 'Account')
        self.assertNotContains(response, 'Admin')
        self.assertContains(response, 'No products found!')

    def test_index_page_two(self):
        '''
        Test index view on page two.
        '''

        products = models.Product.active_objects.all()[12:]
        response = self.client.get('/2/')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['products'],
            map(repr, products),
        )
        self.assertContains(response, 'Home', count=1)
        self.assertContains(response, 'Cart', count=1)
        self.assertContains(response, 'Login', count=1)
        self.assertContains(response, 'Register', count=1)
        self.assertNotContains(response, 'Logout')
        self.assertNotContains(response, 'Account')
        self.assertNotContains(response, 'Admin')

    def test_index_404(self):
        '''
        Test index view to get 404 error by requesting nonexistent page.
        '''

        response = self.client.get('/3/')
        self.assertEqual(response.status_code, 404)

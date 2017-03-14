import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from commerce import models

class TestViews(TestCase):
    def setUp(self):
        product = models.Product.objects.create(
            name='product_1',
            price='1.99',
            description='',
            stock=4,
            image='product_1.jpg',
        )

        User.objects.create_user(
            pk=1,
            username='user_1',
            password='password_1',
        )

        user = User.objects.create_user(
            pk=2,
            username='user_2',
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
            pk=3,
            username='user_3',
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
            pk=4,
            username='user_4',
            password='password_4',
        )
        address = user.addresses.create(
            pk=3,
            street='street_3',
            city='city_3',
            state='S3',
            zip_code='zip_3',
        )
        user.cards.create(
            pk=2,
            card_number='',
            card_type='type_2',
            holder_name='name_2',
            expiration_date=datetime.date.today(),
        )
        order = user.orders.create(
            pk=1,
            street=address.street,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
            total='1.99',
        )
        models.OrderItem.objects.create(
            pk=1,
            order=order,
            product=product,
            purchase_price='1.99',
            quantity=1,
        )

        user = User.objects.create_user(
            pk=5,
            username='user_5',
            password='password_5',
        )
        address = user.addresses.create(
            pk=4,
            street='street_4',
            city='city_4',
            state='S4',
            zip_code='zip_4',
        )
        user.cards.create(
            pk=3,
            card_number='',
            card_type='type_3',
            holder_name='name_3',
            expiration_date=datetime.date.today(),
        )
        order = user.orders.create(
            pk=2,
            street=address.street,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
            total='1.99',
        )
        models.OrderItem.objects.create(
            pk=2,
            order=order,
            product=product,
            purchase_price='1.99',
            quantity=1,
        )
        models.Review.objects.create(
            pk=1,
            product=product,
            user=user,
            title='title_1',
            body='body_1',
            rating=50,
        )

    def test_index_no_address_no_card_no_order_no_review(self):
        user = User.objects.get(username='user_1')
        self.client.force_login(user)

        response = self.client.get('/account/')
        self.assertContains(response, 'Add Address', count=1)
        self.assertContains(response, 'Add Card', count=1)
        self.assertNotContains(response, 'Orders')
        self.assertNotContains(response, 'Reviews')

    def test_index_no_card_no_order_no_review(self):
        user = User.objects.get(username='user_2')
        self.client.force_login(user)

        response = self.client.get('/account/')
        self.assertContains(response, 'Addresses', count=1)
        self.assertContains(response, 'Add Card', count=1)
        self.assertNotContains(response, 'Orders')
        self.assertNotContains(response, 'Reviews')

    def test_index_no_order_no_review(self):
        user = User.objects.get(username='user_3')
        self.client.force_login(user)

        response = self.client.get('/account/')
        self.assertContains(response, 'Addresses', count=1)
        self.assertContains(response, 'Cards', count=1)
        self.assertNotContains(response, 'Orders')
        self.assertNotContains(response, 'Reviews')

    def test_index_no_review(self):
        user = User.objects.get(username='user_4')
        self.client.force_login(user)

        response = self.client.get('/account/')
        self.assertContains(response, 'Addresses', count=1)
        self.assertContains(response, 'Cards', count=1)
        self.assertContains(response, 'Orders', count=1)
        self.assertNotContains(response, 'Reviews')

    def test_index(self):
        user = User.objects.get(username='user_5')
        self.client.force_login(user)

        response = self.client.get('/account/')
        self.assertContains(response, 'Addresses', count=1)
        self.assertContains(response, 'Cards', count=1)
        self.assertContains(response, 'Orders', count=1)
        self.assertContains(response, 'Reviews', count=1)

from django.test import TestCase
from django.contrib.auth.models import User
from .. import models

class ProductTests(TestCase):
    def setUp(self):
        user_1 = User.objects.create_user(
            username='user_1',
            password='password_1',
        )
        user_2 = User.objects.create_user(
            username='user_2',
            password='password_2',
        )
        product_1 = models.Product.objects.create(
            id=1,
            name='product_1',
            price='29.99',
            stock=3,
            description='',
            image='product_1.jpg',
        )
        product_2 = models.Product.objects.create(
            id=2,
            name='product_2',
            price='999.99',
            stock=15,
            description='',
            image='product_2.jpg',
        )
        order_1 = models.Order.objects.create(user=user_1)
        order_2 = models.Order.objects.create(user=user_2)
        models.OrderItem.objects.create(
            product=product_1,
            order=order_1,
            purchase_price=product_1.price,
            quantity=1,
        )
        models.OrderItem.objects.create(
            product=product_1,
            order=order_2,
            purchase_price=product_1.price,
            quantity=2,
        )
        models.Review.objects.create(
            user=user_1,
            product=product_1,
            title='review_1',
            body='',
            rating=78,
        )
        models.Review.objects.create(
            user=user_2,
            product=product_1,
            title='review_2',
            body='',
            rating=98,
        )

    def test_purchase_count(self):
        '''
        Test purchase_count property on product that has 3 purchases.
        '''

        product = models.Product.objects.get(pk=1)
        self.assertEqual(product.purchase_count, 3)

    def test_no_purchase_count(self):
        '''
        Test purchase_count property on product that has not been purchased.
        '''

        product = models.Product.objects.get(pk=2)
        self.assertEqual(product.purchase_count, 0)

    def test_rating(self):
        '''
        Test rating property on product with 2 reviews.
        '''

        product = models.Product.objects.get(pk=1)
        self.assertEqual(product.rating, 88)

    def test_no_rating(self):
        '''
        Test rating property on product with no reviews.
        '''

        product = models.Product.objects.get(pk=2)
        self.assertEqual(product.rating, 0)

    def test_in_stock(self):
        '''
        Test in_stock property on product that is in stock.
        '''

        product = models.Product.objects.get(pk=2)
        self.assertEqual(product.in_stock, True)

    def test_not_in_stock(self):
        '''
        Test in_stock property on product that is not in stock.
        '''

        product = models.Product.objects.get(pk=1)
        self.assertEqual(product.in_stock, False)

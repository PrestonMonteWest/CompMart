from django.test import TestCase, Client
from django.contrib.sites.models import Site
from .. import models

class IndexTests(TestCase):
    def setUp(self):
        for i in range(1, 17):
            models.Product.objects.create(
                name='Product %d' % i,
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

    def test_index_no_query(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

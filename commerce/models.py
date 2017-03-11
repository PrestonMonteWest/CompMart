from threading import Lock
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from account.models import AddressBase, CreditCard

mutex = Lock()

class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(discontinued=False, stock__gt=0)

class Product(models.Model):
    class Meta:
        ordering = ('name',)

    reviewers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Review',
        related_name='reviewed_products'
    )
    name = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(max_length=1000, blank=True)
    discontinued = models.BooleanField(default=False)
    stock = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='images/products')
    objects = models.Manager()
    active_objects = ActiveProductManager()

    def __str__(self):
        return self.name

    @property
    def purchase_count(self):
        from django.db.models import Sum
        return self.orderitem_set.aggregate(Sum('quantity'))['quantity__sum'] or 0

    @property
    def rating(self):
        from django.db.models import Avg
        return round(self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0)

    @property
    def in_stock(self):
        return self.stock > 0

    def get_absolute_url(self):
        return reverse('commerce:product', args=(self.pk,))

class Review(models.Model):
    class Meta:
        ordering = ('-pub_date',)
        unique_together = (('product', 'user'),)

    product = models.ForeignKey(Product, models.CASCADE, related_name='reviews')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name='reviews'
    )
    title = models.CharField(max_length=30)
    body = models.TextField()
    rating = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField('publication date', default=timezone.now)

    def __str__(self):
        return self.title

class Order(AddressBase):
    class Meta:
        ordering = ('-purchase_date',)

    products = models.ManyToManyField(Product, through='OrderItem', related_name='orders')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name='orders',
    )
    card = models.ForeignKey(
        CreditCard,
        models.SET_NULL,
        related_name='orders',
        null=True,
    )
    purchase_date = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=7, decimal_places=2)

    def get_absolute_url(self):
        return reverse('account:order', args=(self.pk,))

    def __str__(self):
        return '{}, {}'.format(self.user, self.purchase_date)

class OrderItem(models.Model):
    class Meta:
        unique_together = (('order', 'product'),)

    order = models.ForeignKey(Order, models.CASCADE)
    product = models.ForeignKey(Product, models.PROTECT)
    purchase_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return '{}, {}'.format(self.order, self.product)

    def save(self, *args, **kwargs):
        mutex.acquire()
        if self.product.stock >= self.quantity:
            self.product.stock -= self.quantity
            self.product.save()
            super().save(*args, **kwargs)
        else:
            raise ValueError('%s is out of stock.' % self.product)
        mutex.release()

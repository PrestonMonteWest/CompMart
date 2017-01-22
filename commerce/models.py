from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class AddressBase(models.Model):
    class Meta:
        abstract = True

    STATES = (
        ('AK', 'Alaska'),
        ('AL', 'Alabama'),
        ('AR', 'Arkansas'),
        ('AS', 'American Samoa'),
        ('AZ', 'Arizona'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DC', 'District of Columbia'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('GU', 'Guam'),
        ('HI', 'Hawaii'),
        ('IA', 'Iowa'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('MA', 'Massachusetts'),
        ('MD', 'Maryland'),
        ('ME', 'Maine'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MO', 'Missouri'),
        ('MP', 'Northern Mariana Islands'),
        ('MS', 'Mississippi'),
        ('MT', 'Montana'),
        ('NA', 'National'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('NE', 'Nebraska'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NV', 'Nevada'),
        ('NY', 'New York'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('PR', 'Puerto Rico'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VA', 'Virginia'),
        ('VI', 'Virgin Islands'),
        ('VT', 'Vermont'),
        ('WA', 'Washington'),
        ('WI', 'Wisconsin'),
        ('WV', 'West Virginia'),
        ('WY', 'Wyoming'),
    )

    street = models.CharField(max_length=60)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2, choices=STATES)
    zip_code = models.CharField(max_length=5)

class Product(models.Model):
    reviewers = models.ManyToManyField(User, through='Review', related_name='reviewed_products')
    name = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(max_length=1000, blank=True)
    discontinued = models.BooleanField(default=False)
    stock = models.PositiveSmallIntegerField()
    purchase_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def in_stock(self):
        return self.stock > 0

    def get_absolute_url(self):
        return reverse('commerce.views.details', args=(str(self.id),))

class Image(models.Model):
    class Meta:
        unique_together = (('product', 'image'),)

    product = models.ForeignKey(Product, models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product/%Y/%m/%d')

    def __str__(self):
        return self.image

class Review(models.Model):
    class Meta:
        unique_together = (('product', 'user'),)

    product = models.ForeignKey(Product, models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=30)
    body = models.TextField()
    rating = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Address(AddressBase):
    class Meta:
        unique_together = (('user', 'street', 'city', 'state'),)

    user = models.ForeignKey(User, models.CASCADE, related_name='addresses')

    def __str__(self):
        return '{}, {}, {} {}'.format(
            self.street,
            self.city,
            self.state,
            self.zip_code
        )

class CreditCard(models.Model):
    class Meta:
        unique_together = (('user', 'card_number'),)

    user = models.ForeignKey(User, models.CASCADE, related_name='cards')
    card_number = models.CharField(max_length=16)
    card_type = models.CharField(max_length=20)
    holder_name = models.CharField(max_length=50)
    expiration_date = models.DateField()

class Order(AddressBase):
    class Meta:
        ordering = ('purchase_date',)

    products = models.ManyToManyField(Product, through='OrderItem', related_name='orders')
    user = models.ForeignKey(User, models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=7, decimal_places=2)
    purchase_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Order #{}'.format(self.id)

class OrderItem(models.Model):
    class Meta:
        unique_together = (('order', 'product'),)

    order = models.ForeignKey(Order, models.CASCADE)
    product = models.ForeignKey(Product, models.PROTECT)
    quantity = models.PositiveSmallIntegerField()

from django.contrib import admin
from . import models

class OrderItemInline(admin.TabularInline):
    fields = ('product', 'quantity')
    raw_id_fields = ('product',)
    model = models.OrderItem
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'stock', 'discontinued')
    search_fields = ('name', 'description')
    list_filter = ('discontinued',)
    fields = ('name', 'description', 'price', 'stock', 'discontinued', 'image')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'title', 'body', 'rating', 'pub_date')
    search_fields = ('title', 'body')
    list_filter = ('pub_date', 'rating')
    date_hierarchy = 'pub_date'
    fields = ('user', 'product', 'title', 'body', 'rating')
    raw_id_fields = ('user', 'product')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'street', 'city', 'state', 'total', 'purchase_date')
    search_fields = ('street', 'city', 'state')
    list_filter = ('purchase_date',)
    date_hierarchy = 'purchase_date'
    fields = ('street', 'city', 'state', 'zip_code')
    inlines = (OrderItemInline,)

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street', 'city', 'state', 'zip_code')
    fields = ('user', 'street', 'city', 'state', 'zip_code')
    raw_id_fields = ('user',)

class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_number', 'holder_name', 'expiration_date')
    fields = ('user', 'card_number', 'holder_name', 'expiration_date')
    raw_id_fields = ('user',)

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.CreditCard, CreditCardAdmin)
admin.site.register(models.Order, OrderAdmin)

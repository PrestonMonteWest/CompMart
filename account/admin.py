from django.contrib import admin
from . import models

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street', 'city', 'state', 'zip_code')
    raw_id_fields = ('user',)
    search_fields = ('street', 'city', 'state', 'zip_code')
    fields = ('user', 'street', 'city', 'state', 'zip_code')

class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_type', 'holder_name', 'expiration_date')
    search_fields = ('card_type', 'holder_name')
    fields = ('user', 'card_number', 'card_type', 'holder_name', 'expiration_date')
    date_hierarchy = 'expiration_date'
    list_filter = ('expiration_date',)

admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.CreditCard, CreditCardAdmin)

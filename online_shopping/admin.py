from online_shopping.views import category
from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.admin.sites import site
from .models import *

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'contact_number', 'city', 'state', 'zipcode', 'image']


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'contact_number', 'gst_number', 'verified', 'rejected','shop_name', 'shop_address', 'image']

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'contact_number', 'dob', 'gender', 'address', 'image']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category']

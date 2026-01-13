from django.contrib import admin
from .models import Category, FAQ, Contact, Products, Order, Store


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('title', 'category__name')
    ordering = ('-created_at',)

admin.site.register(Products, ProductsAdmin)    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('-created_at',)

admin.site.register(Category, CategoryAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'email')
    ordering = ('-created_at',)

admin.site.register(Contact, ContactAdmin)


class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('question',)
    ordering = ('-created_at',)

admin.site.register(FAQ, FAQAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'product__title')

admin.site.register(Order, OrderAdmin)

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')

admin.site.register(Store, StoreAdmin)
    
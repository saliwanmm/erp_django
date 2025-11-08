from django.contrib import admin
from .models import Category, Warehouse, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at")
    search_fields = ("name", )


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "created_at")
    search_fields = ("name", )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "warehouse", "quantity", "price", "created_by")
    list_filter = ("category", "warehouse")
    search_fields = ("name", )
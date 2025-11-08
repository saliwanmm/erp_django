from django.urls import path

from .views import ProductListAPIView, ProductDetailAPIView, CategoryListAPIView, CategoryDetailAPIView, WarehouseListAPIView, WarehouseDetailAPIView

from .views import (
    ProductListView, ProductCreateView, ProductEditView, ProductDeleteView, 
    CategoryListView, CategoryCreateView, CategoryEditView, CategoryDeleteView,WarehouseListView, WarehouseCreateView, WarehouseEditView, WarehouseDeleteView
)


urlpatterns = [
    # ApiViews Product
    path("products/", ProductListAPIView.as_view(), name="products"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product_detail"),
    # ApiViews Category
    path("categories/", CategoryListAPIView.as_view(), name="categories"),
    path("categories/<int:pk>/", CategoryDetailAPIView.as_view(), name="category_detail"),
    # ApiViews Warehouse
    path("warehouses/", WarehouseListAPIView.as_view(), name="warehouses"),
    path("warehouses/<int:pk>/", WarehouseDetailAPIView.as_view(), name="warehouse_detail"),
    # HTMLViews Products
    path("products/html/", ProductListView.as_view(), name=("products_html")),
    path("products/create", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/edit/", ProductEditView.as_view(), name=("product_edit_html")),
    path("products/<int:pk>/delete", ProductDeleteView.as_view(), name="product_delete"),
    # HTMLViews Categories
    path("categories/html/", CategoryListView.as_view(), name="categories_html"),
    path("category/create/", CategoryCreateView.as_view(), name="category_create"),
    path("categories/<int:pk>/edit/", CategoryEditView.as_view(), name=("category_edit_html")),
    path("category/<int:pk>/delete/", CategoryDeleteView.as_view(), name="category_delete"),
    # HTMLViews Warehouses
    path("warehouses/html/", WarehouseListView.as_view(), name=("warehouses_html")),
    path("warehouse/create/", WarehouseCreateView.as_view(), name="warehouse_create"),
    path("warehouse/<int:pk>/edit/", WarehouseEditView.as_view(), name=("warehouse_edit_html")),
    path("warehouses/<int:pk>/delete/", WarehouseDeleteView.as_view(), name="warehouse_delete"),
]

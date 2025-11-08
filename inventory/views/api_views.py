from rest_framework import generics

from ..models import Category, Warehouse, Product
from ..serializers import CategorySerializer, WarehouseSerializer, ProductSerializer
from accounts.permissions import IsManagerOrAdmin


# API Views Products
class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related("category", "warehouse")
    serializer_class = ProductSerializer
    permission_classes = [IsManagerOrAdmin]


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsManagerOrAdmin]


# API Views Categories
class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsManagerOrAdmin]


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsManagerOrAdmin]


# API Views Warehouses
class WarehouseListAPIView(generics.ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsManagerOrAdmin]


class WarehouseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsManagerOrAdmin]
from .base import BaseListView, BaseCreateView, BaseEditView, BaseDeleteView
from .product_views import ProductListView, ProductCreateView, ProductEditView, ProductDeleteView
from .category_views import CategoryListView, CategoryCreateView, CategoryEditView, CategoryDeleteView
from .warehouse_views import WarehouseListView, WarehouseCreateView, WarehouseEditView, WarehouseDeleteView
from .api_views import ProductListAPIView, ProductDetailAPIView, CategoryListAPIView, CategoryDetailAPIView, WarehouseListAPIView, WarehouseDetailAPIView
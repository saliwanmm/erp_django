from django.shortcuts import get_object_or_404

from .base import BaseListView, BaseCreateView, BaseEditView, BaseDeleteView
from ..models import Product, Category, Warehouse


# Products Views
class ProductListView(BaseListView):
    model = Product
    template_name = "inventory/products.html"
    context_name = "products"
    allowed_roles = ["admin", "manager"]

    def get_queryset(self):
        return self.model.objects.select_related("category", "warehouse")


class ProductCreateView(BaseCreateView):
    model = Product
    template_name = "inventory/product_create.html"
    redirect_url_name = "products_html"
    form_fields = ["name", "description", "quantity", "price"]

    extra_context = {
        "categories": Category.objects.all(),
        "warehouses": Warehouse.objects.all(),
    }

    def custom_set_fields(self, obj, request):
        obj.category = Category.objects.get(id=request.POST.get("category"))
        obj.warehouse = Warehouse.objects.get(id=request.POST.get("warehouse"))
        obj.created_by = request.user


class ProductEditView(BaseEditView):
    model = Product
    template_name = "inventory/product_edit.html"
    redirect_url_name = "products_html"
    form_fields = ["name", "description", "price", "quantity"]

    extra_context_fields = {
        "categories": lambda: Category.objects.all(),
        "warehouses": lambda: Warehouse.objects.all(),
    }

    def custom_set_fields(self, obj, request):
        obj.category = get_object_or_404(Category, pk=request.POST.get("category"))
        obj.warehouse = get_object_or_404(Warehouse, pk=request.POST.get("warehouse"))


class ProductDeleteView(BaseDeleteView):
    model = Product
    redirect_url_name = "products_html"
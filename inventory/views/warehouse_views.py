from .base import BaseListView, BaseCreateView, BaseEditView, BaseDeleteView
from ..models import Warehouse


# Warehouses Views
class WarehouseListView(BaseListView):
    model = Warehouse
    template_name = "inventory/warehouses.html"
    context_name = "warehouses"
    allowed_roles = ["admin", "manager"]


class WarehouseCreateView(BaseCreateView):
    model = Warehouse
    template_name = "inventory/warehouse_create.html"
    redirect_url_name = "warehouses_html"
    form_fields = ["name", "location"]


class WarehouseEditView(BaseEditView):
    model = Warehouse
    template_name = "inventory/warehouse_edit.html"
    redirect_url_name = "warehouses_html"
    form_fields = ["name", "location"]


class WarehouseDeleteView(BaseDeleteView):
    model = Warehouse
    redirect_url_name = "warehouses_html"
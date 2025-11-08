from .base import BaseListView, BaseCreateView, BaseEditView, BaseDeleteView
from ..models import Category


# Categories Views
class CategoryListView(BaseListView):
    model = Category
    template_name = "inventory/categories.html"
    context_name = "categories"
    allowed_roles = ["admin", "manager"]


class CategoryCreateView(BaseCreateView):
    model = Category
    template_name = "inventory/category_create.html"
    redirect_url_name = "categories_html"
    form_fields = ["name", "description"]


class CategoryEditView(BaseEditView):
    model = Category
    template_name = "inventory/category_edit.html"
    redirect_url_name = "categories_html"
    form_fields = ["name", "description"]


class CategoryDeleteView(BaseDeleteView):
    model = Category
    redirect_url_name = "categories_html"
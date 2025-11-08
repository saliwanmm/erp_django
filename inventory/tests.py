from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import get_object_or_404
from rest_framework import generics

from .models import Category, Warehouse, Product
from .serializers import CategorySerializer, WarehouseSerializer, ProductSerializer
from accounts.permissions import IsAdmin, IsManagerOrAdmin


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


# Base Category Product Warehouse Views
class BaseEditView(View):
    model = None                 
    template_name = None         
    redirect_url_name = None     
    form_fields = []             
    extra_context_fields = {}    

    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect("login_html")
        if request.user.role != "admin":
            return render(request, "accounts/access_denied.html")

        obj = get_object_or_404(self.model, pk=pk)
        context = {self.context_object_name(): obj}

        for key, value in self.extra_context_fields.items():
            context[key] = value()

        return render(request, self.template_name, context)

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect("login_html")
        if request.user.role != "admin":
            return render(request, "accounts/access_denied.html")

        obj = get_object_or_404(self.model, pk=pk)

        # Задаємо прості поля з POST
        for field in self.form_fields:
            setattr(obj, field, request.POST.get(field))

        # Можливість для підкласів обробити ForeignKey або додаткові поля
        self.custom_set_fields(obj, request)

        obj.save()
        return redirect(self.redirect_url_name)

    # Підклас може переоприділити для кастомної обробки полів
    def custom_set_fields(self, obj, request):
        pass

    def context_object_name(self):
        """Назва ключа для об’єкта у шаблоні. За замовчуванням lowercase назва моделі"""
        return self.model.__name__.lower()


class BaseListView(View):
    model = None                
    template_name = None        
    context_name = None         
    allowed_roles = []          

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login_html")

        if self.allowed_roles and request.user.role not in self.allowed_roles:
            return render(request, "accounts/access_denied.html")

        objects = self.get_queryset()
        context = {self.context_name: objects}
        return render(request, self.template_name, context)

    def get_queryset(self):
        return self.model.objects.all()


class BaseDeleteView(View):
    model = None
    redirect_url_name = None

    def post(self, request, pk):
        if request.user.role != "admin":
            return render(request, "accounts/access_denied.html")
        
        boject = get_object_or_404(self.model, pk=pk)
        boject.delete()

        return redirect(self.redirect_url_name)


class BaseCreateView(View):
    model = None                
    template_name = None        
    redirect_url_name = None    
    form_fields = []            
    extra_context = {}        

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login_html")
        if request.user.role != "admin":
            return render(request, "accounts/access_denied.html")

        context = self.extra_context.copy()
        return render(request, self.template_name, context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("login_html")
        if request.user.role != "admin":
            return render(request, "accounts/access_denied.html")

        obj = self.model()

        for field in self.form_fields:
            value = request.POST.get(field)
            setattr(obj, field, value)

        # ForeignKey fields
        self.custom_set_fields(obj, request)

        obj.save()
        return redirect(self.redirect_url_name)

    # For ForeignKey fields
    def custom_set_fields(self, obj, request):
        pass



    
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

    


from django.views import View
from django.shortcuts import render, redirect, get_object_or_404


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
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect

from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer, UserUpdateSerializer
from .permissions import IsAdmin, IsManagerOrAdmin

User = get_user_model()

# Базова сторінка
def accountsView(request):
    return render(request, "accounts/index.html")


# Реєстрація (доступна всім)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# Список користувачів (тільки для адмінів)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


# CRUD для конкретного користувача (тільки для адмінів)
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAdmin]


# Профіль користувача (для залогінених)
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    

class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                return Response(
                    {"error": "Invalid or expired token."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        logout(request)  # Вихід із Django-сесії

        return Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_205_RESET_CONTENT
        )
    

class LogoutView(View):
    def post(self, request):
        # 1️⃣ Отримуємо refresh токен із сесії (якщо він збережений)
        refresh_token = request.session.get("refresh")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # додає токен у blacklist
            except Exception:
                pass  # якщо токен вже недійсний або не знайдений

        # 2️⃣ Видаляємо JWT токени з сесії
        request.session.pop("access", None)
        request.session.pop("refresh", None)

        # 3️⃣ Розлогінюємо користувача (Django-сесія)
        logout(request)

        # 4️⃣ Перенаправляємо користувача назад на accounts
        return redirect("accounts")


class LoginView(View):
    def get(self, request):
        return render(request, "accounts/login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        if user:
            # 1. Створюємо сесію Django
            login(request, user)
            
            # 2. Генеруємо JWT токени для API
            refresh = RefreshToken.for_user(user)
            request.session["access"] = str(refresh.access_token)
            request.session["refresh"] = str(refresh)
            # 3. Перенаправляємо на головну сторінку або аккаунт
            return redirect("accounts")  # або інший route
            
        else:
            # Якщо невірні дані
            return render(request, "accounts/login.html", {"error": "Invalid credentials"})
        

class SignUpView(View):
    def get(self, request):
        return render(request, "accounts/sign_up.html")
    
    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # 1️⃣ Створюємо нового користувача з роллю "employee"
        if User.objects.filter(username=username).exists():
            return render(request, "accounts/sign_up.html", {"error": "Username already exists."})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role="employee"
        )

        # 2️⃣ Логінимо користувача одразу після реєстрації
        login(request, user)

        # 3️⃣ Перенаправляємо на головну (або сторінку профілю)
        return redirect("accounts")


class UserListHtmlView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login_html")
        
        if request.user.role not in ["admin", "manager"]:
            return render(request, "accounts/access_denied.html")
        
        users = User.objects.all()
        return render(request, "accounts/users.html", {"users": users})
    

class ProfileHtmlView(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect("login_html")
    
        user = User.objects.get(pk=pk)
        return render(request, "accounts/profile.html", {"user": user})
    

class UserEditView(View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        if not (request.user.role == "admin" or request.user.id == user.id ):
            return render(request, "accounts/access_denied.html")
        
        return render(request, "accounts/user_edit.html", {"user": user})
    
    def post(self, request, pk):
        user = User.objects.get(pk=pk)

        if not (request.user.role == "admin" or request.user.id == user.id):
            return render(request, "accounts/access_denied.html")
        
        if request.user.id == user.id and request.user.role != "admin":
            user.email = request.POST.get("email")
        else:
            user.email = request.POST.get("email")
            user.role = request.POST.get("role")

        user.save()

        if request.user.role == "admin":
            return redirect("user_list_html")
        else:
            return redirect("profile_html", user.id)
            

class UserDeleteView(View):
    def post(self, request, pk):
        if request.user.role != "admin":
            return render(request, "accounts/access_denied.html")
        
        user = User.objects.get(pk=pk)
        user.delete()
        return redirect("user_list_html")
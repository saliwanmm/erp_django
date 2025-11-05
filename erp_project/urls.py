from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings


router = routers.DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/accounts/", include("accounts.urls"))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

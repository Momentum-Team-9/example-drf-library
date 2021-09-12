"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api import views as api_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register("books", api_views.BookViewSet, basename="books")
router.register(
    "book_records",
    api_views.BookRecordViewSet,
    basename="book_records",
)
router.register("book_reviews", api_views.BookReviewViewSet, basename="book_reviews")
router.register("auth/users", api_views.UserViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

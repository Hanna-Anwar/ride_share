from rest_framework.routers import DefaultRouter

from django.urls import path,include

from user_app.views import RegisterLoginViewSet


router = DefaultRouter()

router.register("auth", RegisterLoginViewSet, basename="auth")

urlpatterns = [

    path("", include(router.urls)),   # creates /api/auth/register/
]

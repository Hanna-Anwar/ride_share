from django.urls import path,include

from rest_framework.routers import DefaultRouter

from ride_app.views import RideViewSet


router = DefaultRouter()

router.register('rides',RideViewSet,basename="rides")

urlpatterns = [

    path("",include(router.urls))
]
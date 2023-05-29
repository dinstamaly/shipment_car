from django.urls import path, include
from rest_framework import routers
from .views import (
    LocationViewSet,
    CarViewSet,
    ShipmentViewSet,
    NearbyShipmentViewSet,
    LocationUpdateView,
)

router = routers.DefaultRouter()
router.register('locations', LocationViewSet)
router.register('cars', CarViewSet)
router.register('shipments', ShipmentViewSet)
router.register('nearby-shipments', NearbyShipmentViewSet, basename='nearby-shipments')
router.register('update-locations', LocationUpdateView, basename='update-locations')

urlpatterns = [
    path('', include(router.urls)),
]

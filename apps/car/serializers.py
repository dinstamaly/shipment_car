from rest_framework import serializers
from .models import Car, ShipmentCar, Location, Shipment


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class ShipmentCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentCar
        fields = '__all__'

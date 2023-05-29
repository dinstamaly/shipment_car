from django.db import models


class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)


class Car(models.Model):
    unique_number = models.CharField(max_length=5, unique=True)
    current_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    capacity = models.IntegerField()


class Shipment(models.Model):
    pick_up = models.ForeignKey(Location, related_name='pick_up_shipments', on_delete=models.CASCADE)
    delivery = models.ForeignKey(Location, related_name='delivery_shipments', on_delete=models.CASCADE)
    weight = models.IntegerField()
    description = models.TextField()
    cars = models.ManyToManyField(Car, through='ShipmentCar')


class ShipmentCar(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    distance = models.FloatField()

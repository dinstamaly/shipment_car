from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Car)
admin.site.register(models.Location)
admin.site.register(models.Shipment)
admin.site.register(models.ShipmentCar)

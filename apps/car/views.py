from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from geopy.distance import distance as geopy_distance

from .models import Car, ShipmentCar, Location, Shipment
from .serializers import CarSerializer, ShipmentCarSerializer, LocationSerializer, ShipmentSerializer


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    @action(detail=True, methods=['put'])
    def update_location(self, request, pk=None):
        car = self.get_object()
        zip_code = request.data.get('zip_code')
        try:
            location = Location.objects.get(zip_code=zip_code)
            car.current_location = location
            car.save()
            return Response(status=status.HTTP_200_OK)
        except Location.DoesNotExist:
            return Response({'error': 'Location not found.'}, status=status.HTTP_404_NOT_FOUND)


class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

    @action(detail=True, methods=['get', 'delete'])
    def cars_with_distance(self, request, pk=None):
        shipment = self.get_object()

        if request.method == 'GET':
            shipment_cars = ShipmentCar.objects.filter(shipment=shipment)
            serializer = ShipmentCarSerializer(shipment_cars, many=True)
            return Response(serializer.data)

        if request.method == 'DELETE':
            shipment.delete()
            return Response({'message': 'Shipment deleted.'}, status=status.HTTP_204_NO_CONTENT)


class NearbyShipmentViewSet(viewsets.ViewSet):

    def list(self, request):
        weight = request.query_params.get('weight', None)
        miles = request.query_params.get('miles', None)

        if weight is not None and miles is not None:
            try:
                weight = int(weight)
                miles = int(miles)
            except ValueError:
                return Response({'error': 'Invalid weight or miles.'}, status=status.HTTP_400_BAD_REQUEST)

            nearby_shipments = Shipment.objects.filter(weight=weight)
            nearby_shipments_cars = ShipmentCar.objects.filter(shipment__in=nearby_shipments)
            filtered_shipment_cars = []
            for shipment_car in nearby_shipments_cars:
                car_location = shipment_car.car.current_location
                shipment_pickup_location = shipment_car.shipment.pick_up
                distance = geopy_distance(
                    (car_location.latitude, car_location.longitude),
                    (shipment_pickup_location.latitude, shipment_pickup_location.longitude)
                ).miles

                if distance <= miles:
                    shipment_car.distance = distance
                    filtered_shipment_cars.append(shipment_car)

            serializer = ShipmentCarSerializer(filtered_shipment_cars, many=True)
            return Response(serializer.data)

        return Response({'error': 'Weight and miles parameters are required.'}, status=status.HTTP_400_BAD_REQUEST)


class LocationUpdateView(viewsets.ViewSet):

    @action(detail=False, methods=['put'])
    def update_locations(self, request):
        cars = Car.objects.all()
        locations = Location.objects.all()

        for car in cars:
            new_location = locations.exclude(id=car.current_location.id).order_by('?').first()
            car.current_location = new_location
            car.save()

        return Response(status=status.HTTP_200_OK)

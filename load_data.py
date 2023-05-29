import csv
import random
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shipment.settings")
django.setup()

from apps.car.models import Car, Location


def load_data():
    with open('uszips.csv', 'r') as file:
        reader = csv.DictReader(file)
        locations = []
        for row in reader:
            location = Location(
                city=row['city'],
                state=row['state_id'],
                zip_code=row['zip'],
                latitude=row['lat'],
                longitude=row['lng'],
            )
            locations.append(location)

        Location.objects.bulk_create(locations)

    cars = []
    for _ in range(20):
        random_zip_code = random.choice(locations).zip_code
        random_capacity = random.randint(1, 1000)
        random_unique_number = str(random.randint(1000, 9999)) + random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        locations = Location.objects.filter(zip_code=random_zip_code)

        car = Car(
            unique_number=random_unique_number,
            current_location=random.choice(locations),
            capacity=random_capacity,
        )
        cars.append(car)

    Car.objects.bulk_create(cars)


if __name__ == '__main__':
    load_data()


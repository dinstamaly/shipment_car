import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shipment.settings")
django.setup()

from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from apps.car.tasks import update_car_locations


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(update_car_locations, 'interval', minutes=3)
    scheduler.start()

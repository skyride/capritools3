import os

from django.core.management.base import BaseCommand
from django.db import connections

from ...models import *
from ...model_updater import ModelUpdater


class Command(BaseCommand):
    help = "Imports the SDE from fuzzworks sqlite database to our main database"

    def handle(self, *args, **options):
        print("Clear existing SDE")
        os.system("rm /data/sqlite-latest.sqlite*")

        print("Downloading SDE")
        os.system("cd /data && wget https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2")

        print("Decompressing")
        os.system("bzip2 -d /data/sqlite-latest.sqlite.bz2")

        # Get cursor for sde db
        with connections['sde'].cursor() as cursor:
            updater = ModelUpdater(cursor)
            updater.update_model(MarketGroup, "invMarketGroups")
            updater.update_model(Category, "invCategories")
            updater.update_model(Group, "invGroups")
            updater.update_model(Type, "invTypes")
            updater.update_model(AttributeCategory, "dgmAttributeCategories")
            updater.update_model(AttributeType, "dgmAttributeTypes")
            updater.update_model(TypeAttribute, "dgmTypeAttributes", no_key=True)
            updater.update_model(Region, "mapRegions")
            updater.update_model(Constellation, "mapConstellations")
            updater.update_model(System, "mapSolarSystems")
            updater.update_model(SystemJump, "mapSolarSystemJumps", no_key=True)
            updater.update_model(Station, "staStations")

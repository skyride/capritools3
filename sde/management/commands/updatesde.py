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
            updater.update_model_upsert(MarketGroup, "invMarketGroups")
            updater.update_model_upsert(Category, "invCategories")
            updater.update_model_upsert(Group, "invGroups")
            updater.update_model_upsert(Type, "invTypes")
            updater.update_model_upsert(AttributeCategory, "dgmAttributeCategories")
            updater.update_model_upsert(AttributeType, "dgmAttributeTypes")
            updater.update_model_upsert(TypeAttribute, "dgmTypeAttributes", no_key=True)
            updater.update_model_upsert(Region, "mapRegions")
            updater.update_model_upsert(Constellation, "mapConstellations")
            updater.update_model_upsert(System, "mapSolarSystems")
            updater.update_model_upsert(SystemJump, "mapSolarSystemJumps", no_key=True)
            updater.update_model_upsert(Faction, "chrFactions")
            updater.update_model_upsert(Station, "staStations")
            updater.update_model_upsert(MapItem, "mapDenormalize")
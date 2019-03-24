from __future__ import print_function
import sys

from django.db import transaction
from psqlextra.query import ConflictAction

from . import maps

# Defines some functions for importing


# Updates a model from the SDE
class ModelUpdater:
    def __init__(self, cursor):
        self.cursor = cursor

    @transaction.atomic
    def update_model(self, Model, table_name, no_key=False):
        """DEPRECATED in favour of update_model_upsert"""
        print("Updating %s...   " % Model.__name__, end="")
        sys.stdout.flush()

        table_map = getattr(maps, Model.__name__)

        # Get query
        query = self.query_from_map(table_name, table_map)

        # Delete all existing results if we have no key
        if no_key:
            Model.objects.all().delete()

        # Iterate query results
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        bulk = []
        for result in results:
            # Get the database object if it's not a keyless table
            if no_key:
                obj = Model()
                create = True
            else:
                try:
                    obj = Model.objects.get(pk=result[0])
                    create = False
                except Model.DoesNotExist:
                    obj = Model()
                    create = True

            # Iterate table map, setting attributes
            for i, attr in enumerate(map(lambda x: x[0], table_map)):
                setattr(obj, attr, result[i])

            if create:
                bulk.append(obj)
            else:
                obj.save()

        if len(bulk) > 0:
            Model.objects.bulk_create(bulk)

        print("%s objects" % len(results))

    
    @transaction.atomic
    def update_model_upsert(self, Model, table_name, no_key=False):
        """Do model updates using Postgres on_conflict for upserts."""
        print("Updating %s...   " % Model.__name__, end="")
        sys.stdout.flush()

        # Get query
        table_map = getattr(maps, Model.__name__)
        query = self.query_from_map(table_name, table_map)
        # Delete all existing results if we have no key
        if no_key:
            Model.objects.all().delete()

        # Build list of intended objects
        def get_objects():
            self.cursor.execute(query)
            for result in self.cursor.fetchall():
                yield {
                    key: result[i]
                    for i, key in enumerate([x[0] for x in table_map])
                }

        objects = list(get_objects())
        Model.objects.on_conflict(['id'], ConflictAction.UPDATE).bulk_insert(objects)
        print("%s objects" % Model.objects.count())


    # Generates SQL select query from a map
    def query_from_map(self, table_name, table_map):
        cols = ", ".join(
            map(
                lambda x: "`" + x[1] + "`",
                table_map
            )
        )

        sql = "SELECT %s FROM %s" % (
            cols,
            table_name
        )

        return sql

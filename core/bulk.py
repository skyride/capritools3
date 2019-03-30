from datetime import timedelta

from django.utils.timezone import now
from psqlextra.query import ConflictAction
from psqlextra.util import postgres_manager

from .esi import ESI
from .models import Alliance, Corporation, Character
from .utils import chunker


def hydrate(Model, ids, days_until_dehydrated=14):
    """
    Make sure these objects exist in the database.
    Returns the number of dry objects that were hydrated.
    """
    hydrated = set(Model.objects.filter(
        id__in=ids,
        updated__gt=now() - timedelta(days=days_until_dehydrated)
    ).values_list('id', flat=True))
    dry = set(ids) - hydrated

    if len(dry) < 1:
        return 0

    # Resolve dry objects from ESI
    objects = []
    api = ESI()
    for ids in chunker(dry, 1000):
        response = api.post("/latest/universe/names/", json=ids)
        for item in response.json():
            objects.append({
                'id': item['id'],
                'name': item['name']
            })
    with postgres_manager(Model) as manager:
        manager.on_conflict(['id'], ConflictAction.UPDATE).bulk_insert(objects)
    return len(dry)
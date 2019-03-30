from django.db import transaction

from core.bulk import hydrate
from core.esi import ESI
from core.models import Alliance, Corporation, Character
from core.utils import chunker

from .exceptions import LocalscanParseException
from .models import Localscan, LocalscanItem


class LocalscanParser(object):
    """
    Parses localscan text into a localscan object set.
    """
    scan = None

    def __init__(self, text):
        self.text = text


    @transaction.atomic
    def parse(self):
        self.scan = Localscan.objects.create(raw=self.text)

        ids = list(self._names_to_ids(self.text))
        if len(ids) < 1:
            raise LocalscanParseException("No character names found in your paste")
        affiliations = self._ids_to_affiliations(ids)

        # Perform hydration
        alliance_ids = [obj['alliance_id'] for obj in affiliations if 'alliance_id' in obj]
        hydrate(Alliance, alliance_ids)
        corporation_ids = [obj['corporation_id'] for obj in affiliations if 'corporation_id' in obj]
        hydrate(Corporation, corporation_ids)
        character_ids = [obj['character_id'] for obj in affiliations if 'character_id' in obj]
        hydrate(Character, character_ids)

        # Create local scan item entries
        LocalscanItem.objects.bulk_create([
            LocalscanItem(
                scan=self.scan,
                character_id=affiliation.get('character_id', None),
                corporation_id=affiliation.get('corporation_id', None),
                alliance_id=affiliation.get('alliance_id', None),
                faction_id=affiliation.get('faction_id', None)
            )
            for affiliation in affiliations
        ])

        return self.scan


    def _names_to_ids(self, text):
        """
        Translate a set of character names to ids.
        """
        api = ESI()
        for chunk in chunker(set(text.split("\n")), 500):
            response = api.post("/latest/universe/ids/", json=chunk)
            for character in response.json().get('characters', []):
                yield character['id']


    def _ids_to_affiliations(self, ids):
        """
        Translates a set of character ids to affiliation dicts.
        """
        api = ESI()
        for chunk in chunker(set(ids), 500):
            response = api.post("/latest/characters/affiliation/", json=chunk)
            for affiliation in response.json():
                yield affiliation
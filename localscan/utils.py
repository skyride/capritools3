import requests

from django.db import transaction

from core.bulk import hydrate
from core.esi import ESI
from core.models import Alliance, Corporation, Character
from core.utils import chunker

from .exceptions import LocalscanParseException
from .models import Localscan, LocalscanItem, Coalition


class LocalscanParser(object):
    """
    Parses localscan text into a localscan object set.
    """
    scan = None
    coalitions_parsed = True

    def __init__(self, text):
        self.text = text


    @transaction.atomic
    def parse(self):
        self.scan = Localscan.objects.create(raw=self.text)

        ids = list(self._names_to_ids(self.text))
        if len(ids) < 1:
            raise LocalscanParseException("No character names found in your paste")
        affiliations = list(self._ids_to_affiliations(ids))

        # Perform hydration
        alliance_ids = [obj['alliance_id'] for obj in affiliations if 'alliance_id' in obj]
        hydrate(Alliance, alliance_ids)
        corporation_ids = [obj['corporation_id'] for obj in affiliations if 'corporation_id' in obj]
        hydrate(Corporation, corporation_ids)
        character_ids = [obj['character_id'] for obj in affiliations if 'character_id' in obj]
        hydrate(Character, character_ids)
        alliance_coalition_map = self.get_alliance_coalition_map(alliance_ids)

        # Create local scan item entries
        LocalscanItem.objects.bulk_create([
            LocalscanItem(
                scan=self.scan,
                character_id=affiliation.get('character_id', None),
                corporation_id=affiliation.get('corporation_id', None),
                alliance_id=affiliation.get('alliance_id', None),
                faction_id=affiliation.get('faction_id', None),
                coalition=alliance_coalition_map.get(affiliation.get('alliance_id'))
            )
            for affiliation in affiliations
        ])

        return len(ids)


    def _names_to_ids(self, text):
        """
        Translate a set of character names to ids.
        """
        api = ESI()
        for chunk in chunker(text.replace("\r", "").split("\n"), 500):
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


    def get_alliance_coalition_map(self, alliance_ids):
        alliance_ids = set(alliance_ids)
        response = requests.get("http://rischwa.net/api/coalitions/current")
        alliance_coalition_map = {}
        if response.status_code == 200:
            coalition_data = response.json()['coalitions']
            for coalition in coalition_data:
                for alliance in coalition['alliances']:
                    if alliance['id'] in alliance_ids:
                        obj, _ = Coalition.objects.get_or_create(
                            scan=self.scan,
                            _id=coalition['_id'],
                            name=coalition['name'],
                            colour=coalition['color']
                        )
                        alliance_coalition_map[alliance['id']] = obj
        else:
            self.coalitions_parsed = False
        print(alliance_coalition_map)

        return alliance_coalition_map
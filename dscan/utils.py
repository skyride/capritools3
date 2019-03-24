from django.db import transaction
from django.db.models import Count

from sde.models import Type, MapItem

from .exceptions import DscanParseException
from .models import Dscan, DscanObject


class DscanParser(object):
    """
    Parses dscan text into a database object.
    """
    dscan = None

    def __init__(self, text):
        self.text = text

    
    def parse_line(self, line):
        # Dscan lines are columns seperated by tabs
        cols = line.split("\t")
        assert len(cols) == 4

        return DscanObject.objects.create(
            scan=self.dscan,
            type_id=cols[0],
            name=cols[1],
            raw=line
        )

    
    @transaction.atomic
    def parse(self):
        """
        Parses and saves a dscan.
        Returns the number of lines accepted/rejected.
        """
        self.dscan = Dscan.objects.create(
            raw=self.text,
            accepted=0,
            rejected=0
        )

        # A dscan is a table split by new lines and tabs
        for line in self.text.split("\n"):
            try:
                self.parse_line(line)
                self.dscan.accepted += 1
            except:
                self.dscan.rejected += 1

        if self.dscan.accepted < 1:
            raise DscanParseException("Couldn't parse any of the lines in the dscan you provided.")

        self.detect_system()
        
        return self.dscan.accepted, self.dscan.rejected


    def detect_system(self):
        system = self._detect_system()
        if system is not None:
            self.dscan.system = system
            self.dscan.save()

    def _detect_system(self):
        """Detect a solar system based on items in the dscan"""
        # Try celestial matching
        celestial_types = Type.objects.annotate(celestials=Count('map_items')).filter(celestials__gt=0)
        print(celestial_types)
        for object in self.dscan.dscan_objects.filter(type__in=celestial_types):
            celestial = MapItem.objects.filter(type_id=object.type_id, name=object.name).first()
            if celestial is not None:
                return celestial.system
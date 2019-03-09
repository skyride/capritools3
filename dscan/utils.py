from django.db import transaction

from dscan.models import Dscan, DscanObject


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
        return DscanObject(
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
        objects = []
        for line in self.text.split("\n"):
            try:
                objects.append(self.parse_line(line))
                self.dscan.accepted += 1
            except:
                self.dscan.rejected += 1

        # Save dscan
        DscanObject.objects.bulk_create(objects)
        
        return self.dscan.accepted, self.dscan.rejected
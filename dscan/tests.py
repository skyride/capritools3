from django.test import TestCase, Client
from django.http.response import HttpResponseRedirect

from .utils import DscanParser


# Create your tests here.
class DscanParseTest(TestCase):
    dscans = {
        'english': 
"""35833	Lantorn - R.I.P. Etienne Picard	Fortizar	0 m
16213	NSAN3 DIEZ	Caldari Control Tower	-
11567	Autistic Fury	Avatar	23 km
35832	Lantorn - fairy cake	Astrahus	1,134 km
29633	Siseide	Stargate (Minmatar System)	1.3 AU
29633	Vard	Stargate (Minmatar System)	1.3 AU
29633	Dal	Stargate (Minmatar System)	1.3 AU""",
        'russian':
"""35833	Lantorn - R.I.P. Etienne Picard	Fortizar*	0 м
35832	Lantorn - fairy cake	Astrahus*	1,134 км
16213	NSAN3 DIEZ	Caldari Control Tower*	-
29633	Vard*	Stargate (Minmatar System)*	1.3 а.е.
29633	Siseide*	Stargate (Minmatar System)*	1.3 а.е.
29633	Dal*	Stargate (Minmatar System)*	1.3 а.е.
11567	Autistic Fury	Avatar*	23 км""",
        'french':
"""35833	Lantorn - R.I.P. Etienne Picard	Fortizar*	0 m
16213	NSAN3 DIEZ	Tour de contrôle caldari*	-
11567	Autistic Fury	Avatar*	21 km
35832	Lantorn - fairy cake	Astrahus*	1,132 km
29633	Siseide*	Portail stellaire (système minmatar)*	1.3 UA
29633	Vard*	Portail stellaire (système minmatar)*	1.3 UA
29633	Dal*	Portail stellaire (système minmatar)*	1.3 UA""",
        'german':
"""35833	Lantorn - R.I.P. Etienne Picard	Fortizar*	0 m
35832	Lantorn - fairy cake	Astrahus*	1,132 km
16213	NSAN3 DIEZ	Caldari Control Tower*	-
29633	Vard*	Stargate (Minmatar System)*	1.3 AE
29633	Siseide*	Stargate (Minmatar System)*	1.3 AE
29633	Dal*	Stargate (Minmatar System)*	1.3 AE
11567	Autistic Fury	Avatar*	21 km""",
        'japanese':
"""35833	Lantorn - R.I.P. Etienne Picard	フォータイザー*	0m
35832	Lantorn - fairy cake	アシュトラハス*	1,132km
16213	NSAN3 DIEZ	カルダリコントロールタワー*	-
29633	バード*	スターゲート（ミンマターシステム）*	1.3AU
29633	シサイド*	スターゲート（ミンマターシステム）*	1.3AU
29633	ダル*	スターゲート（ミンマターシステム）*	1.3AU
11567	Autistic Fury	アバター*	21km"""
    }

    def test_parse(self):
        c = Client()

        for language, text in self.dscans.items():
            parser = DscanParser(text)
            self.assertTupleEqual((7, 0), parser.parse())

            # Use the fortizar object to check values
            fort_object = parser.dscan.dscan_objects.get(type_id=35833)
            self.assertEqual("Lantorn - R.I.P. Etienne Picard", fort_object.name)

            # Follow a user story of submitting a scan then following the redirect to view it
            self.assertEqual(c.get("/dscan/").status_code, 200)
            response = c.post("/dscan/", {'dscan': text})
            self.assertIsInstance(response, HttpResponseRedirect)
            response = c.get(response.url)
            self.assertEqual(response.status_code, 200)


    def test_exceptions(self):
        from .exceptions import DscanParseException

        self.assertRaises(DscanParseException, DscanParser("").parse)
        self.assertRaises(DscanParseException, DscanParser("asd asd asd asd").parse)
        self.assertRaises(DscanParseException, DscanParser("asd\tasd\t15\tasd").parse)
        self.assertRaises(DscanParseException, DscanParser("\n\n").parse)
        self.assertRaises(DscanParseException, DscanParser("\nasd\n").parse)

        self.assertEqual(DscanParser("29633	ダル*	スターゲート（ミンマターシステム）*	1.3AU\nasd").parse(), (1, 1))
from django.test import TestCase

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
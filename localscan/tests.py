from django.test import TestCase, Client
from django.http.response import HttpResponseRedirect


class LocalscanParseTests(TestCase):
    def test_by_urls(self):
        c = Client()

        self.assertEqual(c.get("/local/").status_code, 200)


    def test_names_to_ids(self):
        from .utils import LocalscanParser
        p = LocalscanParser(None)

        self.assertListEqual(list(p._names_to_ids("Capri Sun KraftFoods")), [93417038])
        self.assertListEqual(
            list(p._names_to_ids("Capri Sun KraftFoods\nCapri Sun SUPERFOODS")),
            [93417038, 94726691])
        self.assertListEqual(list(p._names_to_ids("")), [])

        # Test garbage input gets silently ignored
        self.assertListEqual(list(p._names_to_ids("this name has too many spaces to be a valid eve character name")), [])
        self.assertListEqual(list(p._names_to_ids("this one has *special characters* that would /NEVER/ exist in @EVEOnline")), [])


    def test_ids_to_affiliations(self):
        from .utils import LocalscanParser
        p = LocalscanParser(None)

        self.assertEqual(len(list(p._ids_to_affiliations([93417038]))), 1)
        self.assertEqual(len(list(p._ids_to_affiliations([93417038, 94726691]))), 2)


    def test_parse(self):
        from .exceptions import LocalscanParseException
        from .utils import LocalscanParser

        LocalscanParser("Capri Sun KraftFoods").parse()
        self.assertRaises(LocalscanParseException, LocalscanParser("").parse)

        p = LocalscanParser("Capri Sun KraftFoods")
        self.assertEqual(p.parse(), 1)
        self.assertEqual(p.scan.items.count(), 1)

        p = LocalscanParser("Capri Sun KraftFoods\nDmitri Vakarian")
        self.assertEqual(p.parse(), 2)
        self.assertEqual(p.scan.items.count(), 2)
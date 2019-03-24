from django.test import TestCase, Client
from django.http.response import HttpResponseRedirect


class LocalscanParseTests(TestCase):
    def test_by_urls(self):
        c = Client()

        self.assertEqual(c.get("/local/").status_code, 200)
from django.test import TestCase, Client


class UrlTests(TestCase):
    def test_urls(self):
        c = Client()
        self.assertEqual(200, c.get("/").status_code)
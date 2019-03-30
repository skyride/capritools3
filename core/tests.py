from django.test import TestCase, Client


class UrlTests(TestCase):
    def test_urls(self):
        c = Client()
        self.assertEqual(200, c.get("/").status_code)


class UtilTests(TestCase):
    def test_chunk(self):
        from .utils import chunk

        # Test with lists
        self.assertEqual(0, len(list(chunk([], 500))))
        self.assertEqual(1, len(list(chunk(list(range(0, 1)), 500))))
        self.assertEqual(2, len(list(chunk(list(range(0, 4)), 2))))
        self.assertEqual(3, len(list(chunk(list(range(0, 5)), 2))))

        # Test with generators
        self.assertEqual(0, len(list(chunk(range(0, 0), 500))))
        self.assertEqual(1, len(list(chunk(range(0, 1), 500))))
        self.assertEqual(2, len(list(chunk(range(0, 4), 2))))
        self.assertEqual(3, len(list(chunk(range(0, 5), 2))))
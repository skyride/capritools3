from django.test import TestCase, Client


class UrlTests(TestCase):
    def test_urls(self):
        c = Client()
        self.assertEqual(200, c.get("/").status_code)


class UtilTests(TestCase):
    def test_chunker(self):
        from .utils import chunker

        # Test with lists
        self.assertEqual(0, len(list(chunker([], 500))))
        self.assertEqual(1, len(list(chunker(list(range(0, 1)), 500))))
        self.assertEqual(2, len(list(chunker(list(range(0, 4)), 2))))
        self.assertEqual(3, len(list(chunker(list(range(0, 5)), 2))))

        # Test with generators
        self.assertEqual(0, len(list(chunker(range(0, 0), 500))))
        self.assertEqual(1, len(list(chunker(range(0, 1), 500))))
        self.assertEqual(2, len(list(chunker(range(0, 4), 2))))
        self.assertEqual(3, len(list(chunker(range(0, 5), 2))))
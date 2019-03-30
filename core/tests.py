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

        # Test with sets
        self.assertEqual(0, len(list(chunker(set(), 500))))
        self.assertEqual(1, len(list(chunker(set(range(0, 1)), 500))))
        self.assertEqual(2, len(list(chunker(set(range(0, 4)), 2))))
        self.assertEqual(3, len(list(chunker(set(range(0, 5)), 2))))

        # Test with generators
        self.assertEqual(0, len(list(chunker(range(0, 0), 500))))
        self.assertEqual(1, len(list(chunker(range(0, 1), 500))))
        self.assertEqual(2, len(list(chunker(range(0, 4), 2))))
        self.assertEqual(3, len(list(chunker(range(0, 5), 2))))


    def test_hydration(self):
        from .bulk import hydrate
        from .models import Alliance, Corporation, Character

        self.assertEqual(hydrate(Alliance, [99005065]), 1)
        Alliance.objects.get(id=99005065)
        self.assertEqual(hydrate(Alliance, [99005065]), 0)

        self.assertEqual(hydrate(Corporation, [98040755]), 1)
        Corporation.objects.get(id=98040755)
        self.assertEqual(hydrate(Corporation, [98040755]), 0)

        self.assertEqual(hydrate(Character, [93417038]), 1)
        Character.objects.get(id=93417038)
        self.assertEqual(hydrate(Character, [93417038]), 0)
from django.test import TestCase, override_settings


class TestGetCart(TestCase):
    def setUp(self):
        self.a = 1

    def test_get_cart(self):
        self.assertEqual(self.a, 1)

    def test_get_cart_2(self):
        self.assertEqual(self.a, 1)

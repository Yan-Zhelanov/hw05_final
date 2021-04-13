from django.test import Client, TestCase
from django.urls import reverse

URLS = {
    'author': {'url': reverse('about:author'),
               'expected_url': '/about/author/'},
    'tech': {'url': reverse('about:tech'), 'expected_url': '/about/tech/'},
}


class AboutRoutesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_correct_urls_as_used(self):
        """Проверка использования верных маршрутов страниц about"""
        for url in URLS.values():
            url_adress = url['url']
            with self.subTest(url_adress=url_adress):
                expected_url = url['expected_url']
                self.assertEqual(url_adress, expected_url)

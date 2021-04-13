from django.test import Client, TestCase
from django.urls import reverse

URLS = {
    'author': {'url': reverse('about:author'),
               'expected_template': 'about/about.html'},
    'tech': {'url': reverse('about:tech'),
             'expected_template': 'about/tech.html'},
}


class AboutTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_response_status_code(self):
        """Проверка доступности страниц about"""
        expected_status_code = 200
        for url in URLS.values():
            url_adress = url['url']
            with self.subTest(url_adress=url_adress):
                response = self.guest_client.get(url_adress)
                self.assertEqual(response.status_code, expected_status_code)

    def test_correct_templates_as_used(self):
        """Проверка использования верных шаблонов страниц about"""
        for url in URLS.values():
            url_adress = url['url']
            with self.subTest(url_adress=url_adress):
                response = self.guest_client.get(url_adress)
                expected_template = url['expected_template']
                self.assertTemplateUsed(response, expected_template)

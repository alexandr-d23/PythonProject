from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from url_shortener.forms import UrlForm
from url_shortener.models import User, get_short_url, UrlWithShortcut


class UrlTestCase(TestCase):

    def test_random_code_size(self):
        self.assertTrue(len(get_short_url()) == 12)

    def test_post_url(self):
        username = 'test'
        password = "pass"
        user = User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)
        self.client.post('', {'full_url': 'https://www.youtube.com/'})
        self.assertTrue(UrlWithShortcut.objects.count() == 1)

    def test_create_urls(self):
        User = get_user_model()
        username = 'test'
        password = "pass"
        user = User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)
        full_url = 'https://www.youtube.com/'
        urls_count = 100
        for i in range(urls_count):
            UrlWithShortcut.objects.create(full_url=full_url, user=user, url_shortcut=get_short_url())
        self.assertTrue(UrlWithShortcut.objects.count() == urls_count)

    def test_reduced_url(self):
        User = get_user_model()
        username = 'test'
        password = "pass"
        user = User.objects.create_user(username=username, password=password)

        full_url = 'https://www.youtube.com/'
        UrlWithShortcut.objects.create(full_url=full_url, user=user, url_shortcut=get_short_url())
        response = self.client.get('/' + UrlWithShortcut.objects.get(id=1).url_shortcut)
        self.assertURLEqual(response.url, full_url)


class AuthCase(TestCase):

    def setUp(self):
        username = 'test'
        password = "pass"
        User.objects.create_user(username=username, password=password)

    def test_log_in_success(self):
        username = 'test'
        password = "pass"
        self.client.login(username=username, password=password)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_log_in_fail(self):
        username = 'test'
        password = "error"
        self.client.login(username=username, password=password)
        response = self.client.get('/urls/')
        self.assertEqual(response.status_code, 302)

    def test_sign_in_avaliable(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_sign_up_avaliable(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_sign_in_unavaliable(self):
        username = 'test'
        password = "pass"
        self.client.login(username=username, password=password)
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 302)

    def test_sign_up_unavaliable(self):
        username = 'test'
        password = "pass"
        self.client.login(username=username, password=password)
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 302)

    def test_urls_unavaliable(self):
        response = self.client.get('/urls/')
        self.assertEqual(response.status_code, 302)

    def test_urls_avaliable(self):
        username = 'test'
        password = "pass"
        self.client.login(username=username, password=password)
        response = self.client.get('/urls/')
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_sign_up_view(self):
        response = self.client.get('/register/')
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_home_view(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_urls_view(self):
        username = 'test'
        password = "pass"
        self.client.login(username=username, password=password)
        response = self.client.get('/urls/')
        self.assertTemplateUsed(response, 'urls.html')

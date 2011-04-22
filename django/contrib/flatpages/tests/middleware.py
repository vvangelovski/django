import os
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from django.test import TestCase

class FlatpageMiddlewareTests(TestCase):
    fixtures = ['sample_flatpages']
    urls = 'django.contrib.flatpages.tests.urls'

    def setUp(self):
        self.old_MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES
        flatpage_middleware_class = 'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
        if flatpage_middleware_class not in settings.MIDDLEWARE_CLASSES:
            settings.MIDDLEWARE_CLASSES += (flatpage_middleware_class,)
        self.old_TEMPLATE_DIRS = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = (
            os.path.join(
                os.path.dirname(__file__),
                'templates'
            ),
        )
        self.old_LOGIN_URL = settings.LOGIN_URL
        settings.LOGIN_URL = '/accounts/login/'

    def tearDown(self):
        settings.MIDDLEWARE_CLASSES = self.old_MIDDLEWARE_CLASSES
        settings.TEMPLATE_DIRS = self.old_TEMPLATE_DIRS
        settings.LOGIN_URL = self.old_LOGIN_URL

    def test_view_flatpage(self):
        "A flatpage can be served through a view, even when the middleware is in use"
        response = self.client.get('/flatpage_root/flatpage/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<p>Isn't it flat!</p>")

    def test_view_non_existent_flatpage(self):
        "A non-existent flatpage raises 404 when served through a view, even when the middleware is in use"
        response = self.client.get('/flatpage_root/no_such_flatpage/')
        self.assertEqual(response.status_code, 404)

    def test_view_authenticated_flatpage(self):
        "A flatpage served through a view can require authentication"
        response = self.client.get('/flatpage_root/sekrit/')
        self.assertRedirects(response, '/accounts/login/?next=/flatpage_root/sekrit/')
        User.objects.create_user('testuser', 'test@example.com', 's3krit')
        self.client.login(username='testuser',password='s3krit')
        response = self.client.get('/flatpage_root/sekrit/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<p>Isn't it sekrit!</p>")

    def test_fallback_flatpage(self):
        "A flatpage can be served by the fallback middlware"
        response = self.client.get('/flatpage/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<p>Isn't it flat!</p>")

    def test_fallback_non_existent_flatpage(self):
        "A non-existent flatpage raises a 404 when served by the fallback middlware"
        response = self.client.get('/no_such_flatpage/')
        self.assertEqual(response.status_code, 404)

    def test_fallback_authenticated_flatpage(self):
        "A flatpage served by the middleware can require authentication"
        response = self.client.get('/sekrit/')
        self.assertRedirects(response, '/accounts/login/?next=/sekrit/')
        User.objects.create_user('testuser', 'test@example.com', 's3krit')
        self.client.login(username='testuser',password='s3krit')
        response = self.client.get('/sekrit/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<p>Isn't it sekrit!</p>")

    def test_fallback_flatpage_special_chars(self):
        "A flatpage with special chars in the URL can be served by the fallback middleware"
        fp = FlatPage.objects.create(
            url="/some.very_special~chars-here/",
            title="A very special page",
            content="Isn't it special!",
            enable_comments=False,
            registration_required=False,
        )
        fp.sites.add(1)

        response = self.client.get('/some.very_special~chars-here/')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "<p>Isn't it special!</p>")


class FlatpageMiddlewareAppendSlashTests(TestCase):
    fixtures = ['sample_flatpages']
    urls = 'django.contrib.flatpages.tests.urls'

    def setUp(self):
        self.old_MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES
        flatpage_middleware_class = 'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
        if flatpage_middleware_class not in settings.MIDDLEWARE_CLASSES:
            settings.MIDDLEWARE_CLASSES += (flatpage_middleware_class,)
        self.old_TEMPLATE_DIRS = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = (
            os.path.join(
                os.path.dirname(__file__),
                'templates'
            ),
        )
        self.old_LOGIN_URL = settings.LOGIN_URL
        settings.LOGIN_URL = '/accounts/login/'
        self.old_APPEND_SLASH = settings.APPEND_SLASH
        settings.APPEND_SLASH = True

    def tearDown(self):
        settings.MIDDLEWARE_CLASSES = self.old_MIDDLEWARE_CLASSES
        settings.TEMPLATE_DIRS = self.old_TEMPLATE_DIRS
        settings.LOGIN_URL = self.old_LOGIN_URL
        settings.APPEND_SLASH = self.old_APPEND_SLASH

    def test_redirect_view_flatpage(self):
        "A flatpage can be served through a view and should add a slash"
        response = self.client.get('/flatpage_root/flatpage')
        self.assertRedirects(response, '/flatpage_root/flatpage/', status_code=301)

    def test_redirect_view_non_existent_flatpage(self):
        "A non-existent flatpage raises 404 when served through a view and should not add a slash"
        response = self.client.get('/flatpage_root/no_such_flatpage')
        self.assertEquals(response.status_code, 404)

    def test_redirect_fallback_flatpage(self):
        "A flatpage can be served by the fallback middlware and should add a slash"
        response = self.client.get('/flatpage')
        self.assertRedirects(response, '/flatpage/', status_code=301)

    def test_redirect_fallback_non_existent_flatpage(self):
        "A non-existent flatpage raises a 404 when served by the fallback middlware and should not add a slash"
        response = self.client.get('/no_such_flatpage')
        self.assertEquals(response.status_code, 404)

    def test_redirect_fallback_flatpage_special_chars(self):
        "A flatpage with special chars in the URL can be served by the fallback middleware and should add a slash"
        fp = FlatPage.objects.create(
            url="/some.very_special~chars-here/",
            title="A very special page",
            content="Isn't it special!",
            enable_comments=False,
            registration_required=False,
        )
        fp.sites.add(1)

        response = self.client.get('/some.very_special~chars-here')
        self.assertRedirects(response, '/some.very_special~chars-here/', status_code=301)

    def test_redirect_fallback_flatpage_root(self):
        "A flatpage at / should not cause a redirect loop when APPEND_SLASH is set"
        fp = FlatPage.objects.create(
            url="/",
            title="Root",
            content="Root",
            enable_comments=False,
            registration_required=False,
        )
        fp.sites.add(1)

        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "<p>Root</p>")



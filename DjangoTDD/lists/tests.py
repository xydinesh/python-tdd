"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page

# TODO: Configure your database in settings.py and sync before running tests.

class HomePageTest(TestCase):
    """Tests for the application views."""

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            django.setup()

    def test_root_url_resolves_to_home_page_view(self):
       found = resolve('/')
       self.assertEqual(found.func, home_page)


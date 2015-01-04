"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page
from django.template.loader import render_to_string
from lists.models import Item, List
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

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_string = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_string)

class NewListTest(TestCase):
    def test_saving_a_post_request(self):
        self.client.post(
        '/lists/new',
        data={'item_text': 'A new list item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertIn('A new list item', new_item.text)

    def test_redirects_after_post(self):
        response = self.client.post(
        '/lists/new',
        data={'item_text': 'A new list item'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/{0}/'.format(new_list.id))


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_item(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):

    def test_displays_only_items_for_that_test(self):
        correct_list = List.objects.create()
        Item.objects.create(text='Itemey 1', list=correct_list)
        Item.objects.create(text='Itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/{0}/'.format(correct_list.id))

        self.assertContains(response, 'Itemey 1')
        self.assertContains(response, 'Itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{0}/'.format(list_.id))
        self.assertTemplateUsed(response, 'list.html')

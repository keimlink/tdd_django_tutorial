from urllib import request, response
from django.http import HttpRequest, HttpResponse
from django.urls  import resolve
from django.test import TestCase
from lists.views import home_page
from django.http import HttpResponse
from django.template.loader import render_to_string

from lists.models import Item


class HomePageTest(TestCase):

    def test_root_url_goes_homepage_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_homepage_view_return_correct_values(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_homepage_can_save_post_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
    
    def test_redirect_after_post(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

    def test_displays_all_list_items(self):
        Item.objects.create(text='item1')
        Item.objects.create(text='item2')

        response = self.client.get('/')

        self.assertIn('item1', response.content.decode())
        self.assertIn('item2', response.content.decode())
 

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_item(self):
        first_item = Item()
        first_item.text = 'The first (ever) item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The 2nd item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) item')
        self.assertEqual(second_saved_item.text, 'The 2nd item')

class ListViewTest(TestCase):

    def test_displays_all_items(self):
        Item.objects.create(text='item1')
        Item.objects.create(text='item2')

        response = self.client.get('/')

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')


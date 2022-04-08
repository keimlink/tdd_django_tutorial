from django.urls  import resolve
from django.test import TestCase
from lists.views import home_page

class HomePageTest(TestCase):

    def test_go_to_homepage(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
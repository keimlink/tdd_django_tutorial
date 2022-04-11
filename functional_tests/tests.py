from email import header
from unicodedata import name
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import unittest
import time
from django.test import LiveServerTestCase

class NewVisitorTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])
    
    def test_add_item_and_retrieve_later(self):
        """ToDo List in title and header"""
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        """Add "buy feather" as item"""
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter To-Do item')

        inputbox.send_keys('Buy feather')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        
        # There is still a textbox to add another "fly home with feather" item
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Fly home with feather')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        
        
        # check for correct entries in todo list
        self.check_for_row_in_list_table('1: Buy feather')
        self.check_for_row_in_list_table('2: Fly home with feather')

    
        """after adding, see a personal url and check that to-do is still there"""

        self.fail('finish the test')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
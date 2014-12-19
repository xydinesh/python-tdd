from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from django.test import LiveServerTestCase

class NewVisitorTest(LiveServerTestCase):

  def setUp(self):
    self.browser = webdriver.Firefox()
    self.browser.implicitly_wait(3)

  def tearDown(self):
    self.browser.quit()

  def test_can_start_a_list_and_retrieve_it_later(self):

    self.browser.get(self.live_server_url)

    # She notices the page title and head mention to-do lists
    self.assertIn('To-Do', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('To-Do', header_text)

    # she is invited to enter a to-do item starigth away
    inputbox = self.browser.find_element_by_id('id_new_item')
    self.assertEqual(
      inputbox.get_attribute('placeholder'),
      'Enter to do item'
    )

    # She is typing "Buy peacock feathers" into a text box
    inputbox.send_keys('Buy peacock feathers')
    # When she hits ENTER, the page updates and now the page lists
    # 1: Buy peacock feathers
    inputbox.send_keys(Keys.ENTER)
    edith_list_url = self.browser.current_url
    self.assertRegex(edith_list_url, '/lists/.+')
    # send_keys is selenium way of input text
    self.check_for_row_in_list_table('1: Buy peacock feathers')

    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Use peacock feathers to make a fly')
    inputbox.send_keys(Keys.ENTER)

    self.check_for_row_in_list_table('1: Buy peacock feathers')
    self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

    # Now a new user, Francis, comes along to the site
    self.browser.quit()
    seld.browser = webdriver.Firefox()

    # Francis visit the home page. There is no sign of Edith's list
    

    # The page updates again, and now show both items on her list

  def check_for_row_in_list_table(self, row_text):
    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    return self.assertIn(row_text, [row.text for row in rows])

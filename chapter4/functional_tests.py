from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):
  def setUp(self):
    self.browser = webdriver.Firefox()

  def tearDown(self):
    self.browser.quit()

  def test_can_start_a_list_and_retrieve_it_later(self):
    # Richard has heard about a new web app for To-Do lists. He goes
    # to check its homepage
    self.browser.get('http://localhost:8000')

    # He notices the page title mentions To-Do list
    self.assertIn('To-Do', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('To-Do', header_text)

    # The page invites him to enter to-do items.
    input_box = self.browser.find_element_by_id('id_new_item')
    self.assertEqual(
      input_box.get_attribute('placeholder'),
      'Enter a to-do item'
    )

    # He types "Read and practice chapter 1 of TDD" in a text box.
    input_box.send_keys('Read and practice chapter 1 of TDD')
    # When he hits enter, the item is updated in the To-Do list:
    # "1: Read and practice chapter 1 of TDD".
    input_box.send_keys(Keys.ENTER)
    time.sleep(1)

    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertTrue(
      any(row.text == '1: Read and practice chapter 1 of TDD' for row in rows)
    )

    # He sees he can enter another item so he enters:
    # "Create a new repository in GitHub and push Chapter 1 code"
    # The page updates his 2nd item in To-Do list.
    self.fail('Stop, to be tested later!')

    # The page has generated a URL, Richard visits the URL and see his To-Do
    # list with 2 items. Confirm the web app works, he goes back to practice
    # TDD.

if __name__ == '__main__':
  unittest.main(warnings='ignore')

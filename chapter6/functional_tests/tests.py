from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10 # Maximum waiting time to catch glitchers or random slowness

class NewVisitorTest(LiveServerTestCase):
  def setUp(self):
    self.browser = webdriver.Firefox()

  def tearDown(self):
    self.browser.quit()

  def wait_for_row_in_list_table(self, row_text):
    start_time = time.time()
    while True:
      try:
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
        return
      except (AssertionError, WebDriverException) as e:
        if time.time() - start_time > MAX_WAIT:
          raise e
        time.sleep(.5)

  def test_can_start_a_list_and_retrieve_it_later(self):
    # Richard has heard about a new web app for To-Do lists. He goes
    # to check its homepage
    self.browser.get(self.live_server_url)

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
    #time.sleep(2)
    self.wait_for_row_in_list_table('1: Read and practice chapter 1 of TDD')

    # He sees he can enter another item so he enters:
    # "Create a new repository in GitHub and push"
    input_box = self.browser.find_element_by_id('id_new_item')
    input_box.send_keys('Create a new repository in GitHub and push')
    input_box.send_keys(Keys.ENTER)
    #time.sleep(2)
    # The page updates and shows the list
    self.wait_for_row_in_list_table('1: Read and practice chapter 1 of TDD')
    self.wait_for_row_in_list_table('2: Create a new repository in GitHub and push')

    # The page has generated a URL, Richard visits the URL and see his To-Do
    # list with 2 items.
    

    # Confirm the web app works, he goes back to practice TDD.
    self.fail('Finish the test!')

if __name__ == '__main__':
  unittest.main(warnings='ignore')

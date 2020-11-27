from selenium import webdriver
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
    self.fail('Finish the test with assert fail!')

    # The page invites him to enter to-do items. He types "Read and practice
    # chapter 1 of TDD" in a text box.
    # When he hits enter, the item is updated in the To-Do list:
    # "1: Read and practice chapter 1 of TDD".

    # He sees he can enter another item so he enters:
    # "Create a new repository in GitHub and push Chapter 1 code"
    # The page updates his 2nd item in To-Do list.

    # The page has generated a URL, Richard visits the URL and see his To-Do
    # list with 2 items. Confirm the web app works, he goes back to practice
    # TDD.

if __name__ == '__main__':
  unittest.main(warnings='ignore')

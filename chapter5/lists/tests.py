from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item

class HomePageTest(TestCase):
  def test_root_url_resolves_to_homepage_view(self):
    found = resolve('/')
    self.assertEqual(found.func, home_page)

  def test_homepage_returns_correct_html(self):
    ''' Manual way to test the right template 
    - The problem with this manual test is that it tests
      constant string value of html.
    - Testing rule: Do not test constant value!
    '''
    request = HttpRequest()
    response = home_page(request)
    html = response.content.decode('utf8')
    # use render_to_string to test html 
    #expected_html = render_to_string('home.html')
    #self.assertEqual(html, expected_html)

    # Manually test html
    self.assertTrue(html.startswith('<html>'))
    self.assertIn('<title>To-Do lists</title>', html)
    self.assertTrue(html.strip().endswith('</html>'))

  def test_uses_home_template(self):
    ''' Use Django Test Client to test the template '''
    # Call self.client.get to pass the testing URL
    response = self.client.get('/')
    self.assertTemplateUsed(response, 'home.html')

  def test_can_save_a_POST_request(self):
    response = self.client.post('/', data={'item_text': 'A new list item'})
    self.assertIn('A new list item', response.content.decode())
    self.assertTemplateUsed(response, 'home.html')


class ItemModelTest(TestCase):
  def test_save_and_retrieve_items(self):
    first_item = Item()
    first_item.text = 'The first (ever) list item'
    first_item.save()
    second_item = Item()
    second_item.text = 'Second item'
    second_item.save()
    saved_items = Item.objects.all()
    
    self.assertEqual(saved_items.count(), 2)
    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    self.assertEqual(first_saved_item.text, 'The first (ever) list item')
    self.assertEqual(second_saved_item.text, 'Second item')

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page

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

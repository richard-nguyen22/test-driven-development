from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item

class HomePageTest(TestCase):
  def test_uses_home_template(self):
    ''' Use Django Test Client to test the template '''
    # Call self.client.get to pass the testing URL
    response = self.client.get('/')
    self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):
  def test_use_list_template(self):
    response = self.client.get('/lists/the-only-list-in-the-world/')
    self.assertTemplateUsed(response, 'list.html')

  def test_display_all_list_items(self):
    Item.objects.create(text='item 1')
    Item.objects.create(text='item 2')
    response = self.client.get('/lists/the-only-list-in-the-world/')
    self.assertContains(response, 'item 1')
    self.assertContains(response, 'item 2')


class ItemModelTest(TestCase):
  def test_save_and_retrieve_items(self):
    first_item = Item()
    first_item.text = 'The 1st ever item'
    first_item.save()
    second_item = Item()
    second_item.text = 'Second item'
    second_item.save()
    saved_items = Item.objects.all()

    self.assertEqual(saved_items.count(), 2)
    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    self.assertEqual(first_saved_item.text, 'The 1st ever item')
    self.assertEqual(second_saved_item.text, 'Second item')


class NewListTest(TestCase):
  def test_can_save_a_POST_request(self):
    response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
    # Check Item contains text
    self.assertEqual(Item.objects.count(), 1)
    new_item = Item.objects.first()
    # Check content of text item
    self.assertEqual(new_item.text, 'A new list item')

  def test_redirect_after_POST(self):
    response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
    self.assertRedirects(response, '/lists/the-only-list-in-the-world/')


from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List

class HomePageTest(TestCase):
  def test_uses_home_template(self):
    ''' Use Django Test Client to test the template '''
    # Call self.client.get to pass the testing URL
    response = self.client.get('/')
    self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):
  def test_use_list_template(self):
    list_ = List.objects.create()
    response = self.client.get(f'/lists/{list_.id}/')
    self.assertTemplateUsed(response, 'list.html')

  def test_display_items_for_that_list(self):
    correct_list = List.objects.create()
    Item.objects.create(text='item 1', list=correct_list)
    Item.objects.create(text='item 2', list=correct_list)
    other_list = List.objects.create()
    Item.objects.create(text='other item 1', list=other_list)
    Item.objects.create(text='other item 2', list=other_list)

    response = self.client.get(f'/lists/{correct_list.id}/')

    self.assertContains(response, 'item 1')
    self.assertContains(response, 'item 2')
    self.assertNotContains(response, 'other item 1')
    self.assertNotContains(response, 'other item 2')

  def test_pass_correct_list_to_template(self):
    other_list = List.objects.create()
    correct_list = List.objects.create()
    response = self.client.get(f'/lists/{correct_list.id}/')
    self.assertEqual(response.context['list'], correct_list)


class ListAndItemModelTest(TestCase):
  def test_save_and_retrieve_items(self):
    list_ = List()
    list_.save()

    first_item = Item()
    first_item.text = 'The 1st ever item'
    first_item.list = list_
    first_item.save()
    second_item = Item()
    second_item.text = 'Second item'
    second_item.list = list_
    second_item.save()

    saved_list = List.objects.first()
    self.assertEqual(saved_list, list_)
    saved_items = Item.objects.all()
    self.assertEqual(saved_items.count(), 2)

    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    self.assertEqual(first_saved_item.text, 'The 1st ever item')
    self.assertEqual(first_saved_item.list, list_)
    self.assertEqual(second_saved_item.text, 'Second item')
    self.assertEqual(second_saved_item.list, list_)


class NewItemTest(TestCase):
  def test_can_save_a_POST_request_to_an_existing_list(self):
    other_list = List.objects.create()
    correct_list = List.objects.create()
    self.client.post(f'/lists/{correct_list.id}/add_item',
      data={'item_text': 'A new item for an existing list'})
   
    # Check Item contains text
    self.assertEqual(Item.objects.count(), 1)
    new_item = Item.objects.first()
    self.assertEqual(new_item.text, 'A new item for an existing list')
    self.assertEqual(new_item.list, correct_list)

  def test_redirect_to_list_view(self):
    other_list = List.objects.create()
    correct_list = List.objects.create()

    response = self.client.post(f'/lists/{correct_list.id}/add_item',
      data={'item_text': 'A new item for an existing list'})
    self.assertRedirects(response, f'/lists/{correct_list.id}/')


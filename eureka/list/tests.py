# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import List
from django.contrib.auth.models import User
from eureka.list.forms import ListForm,ItemForm

class ListCase(TestCase):
    def setUp(self):
        self.user_author = User.objects.create(email="autor@mail.com",username="autor")
        self.one_list = List.objects.create(name="ToDo One", author=self.user_author,priority=3)

    def test_list_author(self):
        """Cantidad de autores"""

        one_list = List.objects.get(name="ToDo One")
        self.assertEqual(one_list.count_by_author(one_list.author), 1)
        self.assertEqual(
        	self.one_list.count_by_author(self.one_list.author),
        	one_list.count_by_author(one_list.author))

    def test_list_equal_by_name(self):
        """Por el mismo nombre"""

        one_list = List.objects.get(name="ToDo One")
        self.assertEqual(one_list,self.one_list)

    def test_list_priority(self):
        """Prioridad limitada 1-4"""
        self.assertTrue(self.one_list.priority >= 0 and self.one_list.priority <= 4)


    def test_forms(self):
        form_data_list = {
            'name': 'ToDo Two',
            'priority':1
        }
        form_list = ListForm(data=form_data_list)

        form_data_item = {
            'title': 'ToDo Two',
            'priority':1,
            'assigned_to':self.user_author.id,
            'note':'Create one reporte for the project',
            'list':self.one_list
        }
        form_item = ListForm(data=form_data_item)
        self.assertTrue(form_list.is_valid())
        #self.assertTrue(form_item.is_valid())





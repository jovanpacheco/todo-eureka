# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import List
from django.contrib.auth.models import User


class ListCase(TestCase):
    def setUp(self):
        User.objects.create(email="autor@mail.com",username="autor")
        List.objects.create(name="ToDo One", author_id=1,priority=5)

    def test_list_author(self):
        """Cantidad de autores"""

        one_list = List.objects.get(name="ToDo One")
        self.assertEqual(one_list.count_by_author(one_list.author), 1)
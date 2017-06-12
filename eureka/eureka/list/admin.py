# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from .models import List,Item,Comment

admin.site.register(List)
admin.site.register(Item)
admin.site.register(Comment)
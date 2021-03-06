# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.template.defaultfilters import slugify
import datetime
import uuid as uuid_lib


class TimeStampedModel(models.Model):
	"""
	An abstract base class model that provides selfupdating
	"""
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	class Meta:
		abstract = True

class Authorable(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_by+')
    
    class Meta:
        abstract = True

PRIORITY_CHOICE = (
    (1,'high'),
    (2,'medium'),
    (3,'normal'),
    (4,'low'),
)

@python_2_unicode_compatible
class List(TimeStampedModel,Authorable):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=100)
    priority = models.PositiveIntegerField(choices=PRIORITY_CHOICE)
    active = models.BooleanField(default=True)
    uuid = models.UUIDField( # Used by the API to look up the record
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(List, self).save(*args, **kwargs)

    @property
    def get_priority(self):
        if self.priority == 1:
            return 'high'
        elif self.priority == 2:
            return 'medium'
        elif self.priority == 3:
            return 'normal'
        elif self.priority == 4:
            return 'low'


    def __str__(self):
        return self.name

    def count_by_author(self,author):
        return List.objects.filter(active=True,author=self.author).count()

    def incomplete_tasks(self):
        # Count all incomplete tasks on the current list instance
        return Item.objects.filter(list=self, completed=0)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Lists"
        # Prevents creation of two lists with the same name in the same author
        unique_together = ("author", "slug")


@python_2_unicode_compatible
class Item(TimeStampedModel,Authorable):
    title = models.CharField(max_length=140)
    list = models.ForeignKey('List')
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(blank=True, null=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='todo_assigned_to')
    note = models.TextField()
    priority = models.PositiveIntegerField(choices=PRIORITY_CHOICE)
    active = models.BooleanField(default=True)
    uuid = models.UUIDField( # Used by the API to look up the record
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False)

    def overdue_status(self):
        "Returns whether the item's due date has passed or not."
        if self.due_date and datetime.date.today() > self.due_date:
            return 1

    @property
    def get_priority(self):
        if self.priority == 1:
            return 'high'
        elif self.priority == 2:
            return 'medium'
        elif self.priority == 3:
            return 'normal'
        elif self.priority == 4:
            return 'low'
            
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('todo-task_detail', kwargs={'task_id': self.id, })

    # Auto-set the item creation / completed date
    def save(self):
        # If Item is being marked complete, set the completed_date
        if self.completed:
            self.completed_date = datetime.datetime.now()
        super(Item, self).save()

    class Meta:
        ordering = ["priority"]


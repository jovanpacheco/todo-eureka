# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
import datetime

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

@python_2_unicode_compatible
class List(TimeStampedModel,Authorable):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=100)
    priority = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def incomplete_tasks(self):
        # Count all incomplete tasks on the current list instance
        return Item.objects.filter(list=self, completed=0)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Lists"
        # Prevents creation of two lists with the same name in the same owner
        unique_together = ("author", "slug")


@python_2_unicode_compatible
class Item(TimeStampedModel,Authorable):
    title = models.CharField(max_length=140)
    list = models.ForeignKey(List)
    due_date = models.DateField(blank=True, null=True, )
    completed = models.BooleanField(default=None)
    completed_date = models.DateField(blank=True, null=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='todo_assigned_to')
    note = models.TextField(blank=True, null=True)
    priority = models.PositiveIntegerField()

    # Has due date for an instance of this object passed?
    def overdue_status(self):
        "Returns whether the item's due date has passed or not."
        if self.due_date and datetime.date.today() > self.due_date:
            return 1

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


@python_2_unicode_compatible
class Comment(TimeStampedModel,Authorable):
    """
    Not using Django's built-in comments because we want to be able to save
    a comment and change task details at the same time. Rolling our own since it's easy.
    """
    task = models.ForeignKey(Item)
    body = models.TextField(blank=True)

    def snippet(self):
        # Define here rather than in __str__ so we can use it in the admin list_display
        return "{author} - {snippet}...".format(author=self.author, snippet=self.body[:35])

    def __str__(self):
        return self.snippet
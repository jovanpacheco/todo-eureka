# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic.list import ListView as ListViewGeneric
from .models import List

class ListView(LoginRequiredMixin, ListViewGeneric):
    model = List
    login_url = '/login/'

    def get_queryset(self):
        qs = super(ListView, self).get_queryset().filter(
            author__id=self.request.user.id
        )

        hide = self.request.GET.get('hide')
        if hide == 'complete':
            qs = qs.filter(is_done=False)

        return qs.order_by('priority')



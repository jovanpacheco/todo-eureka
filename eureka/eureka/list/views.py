# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView, UpdateView, DeleteView,CreateView
from django.views.generic.list import ListView as ListViewGeneric
from django.contrib.messages.views import SuccessMessageMixin
from .models import List
from .forms import ListForm


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


class RegisterView(LoginRequiredMixin,SuccessMessageMixin,CreateView): 
    login_url = '/login/'
    form_class = ListForm
    success_url = reverse_lazy('list_app:list')
    succes_message = "Registrado exitosamente"
    template_name = 'list/list_register.html'


    def form_valid(self, form):
        return super(RegisterView, self).form_valid(form)

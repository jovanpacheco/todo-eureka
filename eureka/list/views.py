# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import FormView, UpdateView, DeleteView,CreateView
from django.views.generic.list import ListView as ListViewGeneric
from django.contrib.messages.views import SuccessMessageMixin
from .models import List, Item
from .forms import ListForm
from django.http import Http404

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
    success_message = "Registrado exitosamente"
    template_name = 'list/list_register.html'


    def form_valid(self, form):
        return super(RegisterView, self).form_valid(form)


class ListUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = List
    fields = ['name', 'active', 'priority']
    success_url = reverse_lazy('list_app:list')
    success_message = "Actualizado exitosamente"
    login_url = '/login/'
    redirect_field_name = 'redirect_to'



class ListDetailView(DetailView):
 
    model = List

    def get_object(self, queryset=None):
        obj = super(ListDetailView, self).get_object()
        if not obj.author == self.request.user:
            raise Http404
        return obj


class ListDeleteView(DeleteView):

    model = List
    success_url = reverse_lazy('list_app:list')  




class ItemListView(LoginRequiredMixin, ListViewGeneric):
    model = Item
    login_url = '/login/'

    def get_queryset(self):
        qs = super(ItemListView, self).get_queryset()
        qs.filter(list_id=self.kwargs['pk'])
        return qs    
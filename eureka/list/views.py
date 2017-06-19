# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView,RedirectView
from django.views.generic.edit import FormView, UpdateView, DeleteView,CreateView
from django.views.generic.list import ListView as ListViewGeneric
from django.contrib.messages.views import SuccessMessageMixin
from .models import List, Item
from .forms import ListForm,ItemForm

class ListRetriveView(LoginRequiredMixin, ListViewGeneric):
    model = List
    login_url = '/login/'

    def get_queryset(self):
        qs = super(ListRetriveView, self).get_queryset().filter(
            author__id=self.request.user.id
        )

        hide = self.request.GET.get('hide')
        if hide == 'complete':
            qs = qs.filter(is_done=False)

        return qs.order_by('priority')


class ListRegisterView(LoginRequiredMixin,SuccessMessageMixin,CreateView): 
    login_url = '/login/'
    form_class = ListForm
    success_url = reverse_lazy('list_app:list_list')
    success_message = "Registrado exitosamente"
    template_name = 'list/list_register.html'

    def form_valid(self, form):
        return super(ListRegisterView, self).form_valid(form)


class ListUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = List
    fields = ['name', 'active', 'priority']
    success_url = reverse_lazy('list_app:list_list')
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
    success_url = reverse_lazy('list_app:list_list')  




class ItemListView(LoginRequiredMixin, ListViewGeneric):
    model = Item
    login_url = '/login/'
    template_name = 'item/item_list.html'

    def get_queryset(self):
        try:
            List.objects.get(id=self.kwargs['pk'])
            return Item.objects.filter(list_id=self.kwargs['pk'])
        except List.DoesNotExist:
            raise Http404
        

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['pk_list'] = self.kwargs['pk']
        return context  


class ItemRegisterView(LoginRequiredMixin,SuccessMessageMixin,CreateView): 
    login_url = '/login/'
    success_message = "Registrado exitosamente"
    template_name = 'item/item_register.html'

    def get_success_url(self, **kwargs):
        try:
            return reverse_lazy('list_app:item_list',kwargs={'pk':self.kwargs['pk']})
        except KeyError:
            return reverse_lazy('list_app:list_list')

    def form_valid(self, form):
        try:
            form.instance.list = List.objects.get(id=self.kwargs['pk'])
        except KeyError:
            pass     
        return super(ItemRegisterView, self).form_valid(form)
        
class ItemUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Item
    fields = ['title','list','note','priority','author']
    success_message = "Actualizado exitosamente"
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'item/item_form.html'    

    def get_success_url(self, **kwargs):
        return reverse_lazy('list_app:item_list',kwargs={'pk':self.kwargs['pk_list']})

class ItemDeleteView(DeleteView):

    model = Item
    template_name = 'item/item_confirm_delete.html' 
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('list_app:item_list',kwargs={'pk':self.kwargs['pk_list']})    


class ItemCompleted(RedirectView):

    def get_redirect_url(self, **kwargs):
        try:
            item = Item.objects.get(id=self.kwargs['pk'])
            item.completed = True
            item.save()

            return reverse_lazy('list_app:item_list',kwargs={'pk':self.kwargs['pk_list']}) 
        except item.DoesNotExist:
            raise Http404

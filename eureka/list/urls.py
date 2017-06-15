from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from .views import (
	ListRetriveView,ListRegisterView,ListUpdateView,ListDetailView,ListDeleteView,
	ItemListView,ItemRegisterView,ItemUpdateView,ItemDeleteView,ItemCompleted
)

from django.contrib.auth.decorators import login_required
from .forms import ItemForm,ItemListForm

urlpatterns = [
	url(r'^$',TemplateView.as_view(template_name='index.html') , name="index"),

	url(r'^list/$',ListRetriveView.as_view() , name="list_list"),
	url(r'^list/register/$',ListRegisterView.as_view() , name="list_register"),
	url(r'^list/update/(?P<pk>\d+)/$', ListUpdateView.as_view(), name='list_update'),
	url(r'^list/detail/(?P<pk>\d+)/$', ListDetailView.as_view(), name='list_detail'),
	url(r'^list/delete/(?P<pk>\d+)/$', ListDeleteView.as_view(), name='list_delete'),

	url(r'^item/list/(?P<pk>\d+)/$',ItemListView.as_view() , name="item_list"),
	url(r'^item/list/register/(?P<pk>\d+)/$',ItemRegisterView.as_view(form_class=ItemListForm) , name="item_register_list"),
	url(r'^item/register/$',ItemRegisterView.as_view(form_class=ItemForm) , name="item_register_new"),
	url(r'^item/list/(?P<pk_list>\d+)/update/(?P<pk>\d+)/$', ItemUpdateView.as_view(), name='item_update'),
	url(r'^item/list/(?P<pk_list>\d+)/delete/(?P<pk>\d+)/$', ItemDeleteView.as_view(), name='item_delete'),
	url(r'^item/list/(?P<pk_list>\d+)/completed/(?P<pk>\d+)/$', ItemCompleted.as_view(), name='item_completed')

]
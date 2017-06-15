from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from .views import (
	ListView,RegisterView,ListUpdateView,ListDetailView,ListDeleteView,
	ItemListView
)

from django.contrib.auth.decorators import login_required

urlpatterns = [
	url(r'^$',TemplateView.as_view(template_name='index.html') , name="index"),

	url(r'^list/$',ListView.as_view() , name="list_list"),
	url(r'^list/register/$',RegisterView.as_view() , name="list_register"),
	url(r'^list/update/(?P<pk>\d+)/$', ListUpdateView.as_view(), name='list_update'),
	url(r'^list/detail/(?P<pk>\d+)/$', ListDetailView.as_view(), name='list_detail'),
	url(r'^list/delete/(?P<pk>\d+)/$', ListDeleteView.as_view(), name='list_delete'),

	url(r'^item/(?P<pk>\d+)/$',ItemListView.as_view() , name="list_item"),
]



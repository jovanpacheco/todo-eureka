from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
#from django.views.generic import TemplateView
from .views import ListView
from django.contrib.auth.decorators import login_required

urlpatterns = [
	url(r'^$',ListView.as_view() , name="list"),
]

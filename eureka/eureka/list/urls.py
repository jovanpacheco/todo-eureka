from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
	url(r'^$',TemplateView.as_view(template_name="index.html") , name="index"),
]

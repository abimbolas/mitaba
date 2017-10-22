from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'entries', views.EntryView.as_view())
]

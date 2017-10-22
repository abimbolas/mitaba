from django.conf.urls import url
from . import views

# Endpoints
urlpatterns = [
    url(r'profile', views.ProfileView.as_view())
]

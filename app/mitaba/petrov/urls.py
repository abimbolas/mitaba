from django.conf.urls import url
from . import views

# Endpoints
urlpatterns = [
    url(r'petrov', views.PetrovView.as_view())
]

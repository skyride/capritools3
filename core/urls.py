from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = "dscan"
urlpatterns = [
    path("", TemplateView.as_view(template_name="core/home.html"), name="home")
]

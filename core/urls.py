from django.urls import path

from . import views

app_name = "dscan"
urlpatterns = [
    path("", views.home)
]
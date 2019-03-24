from django.urls import path

from . import views


app_name = "dscan"
urlpatterns = [
    path("", views.DscanSubmit.as_view(), name="submit"),
    path("<str:key>", views.view, name="view")
]
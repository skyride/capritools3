from django.urls import path

from . import views


app_name = "pastebin"
urlpatterns = [
    path("", views.Submit.as_view(), name="submit"),
    #path("<str:key>", views.LocalscanView.as_view(), name="view")
]
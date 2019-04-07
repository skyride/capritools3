from django.urls import path
from django.views.decorators.cache import cache_page

from . import views


app_name = "localscan"
urlpatterns = [
    path("", views.LocalscanSubmit.as_view(), name="submit"),
    path("<str:key>", views.LocalscanView.as_view(), name="view")
]
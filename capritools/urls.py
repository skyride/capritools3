from django.views.generic import TemplateView
from django.urls import path, include


urlpatterns = [
    path("", TemplateView.as_view(template_name="core/home.html"), name="home"),
    path("dscan/", include('dscan.urls', namespace="dscan")),
    path("local/", include('localscan.urls', namespace="localscan")),
    path("paste/", include('pastebin.urls', namespace="pastebin"))
]

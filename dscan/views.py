from django.views import View
from django.shortcuts import render


class DscanSubmit(View):
    """Submit a new dscan"""
    def get(self, request):
        return render(request, "dscan/submit.html")
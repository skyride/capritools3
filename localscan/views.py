from django.shortcuts import render
from django.views import View


class LocalscanSubmit(View):
    """Submit a new local scan"""
    def get(self, request):
        return render(request, "localscan/submit.html")
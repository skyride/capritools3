from django.contrib import messages
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect

from .exceptions import LocalscanParseException
from .models import Localscan
from .utils import LocalscanParser


class LocalscanSubmit(View):
    """Submit a new local scan"""
    def get(self, request):
        return render(request, "localscan/submit.html")

    def post(self, request):
        if "localscan" not in request.POST:
            messages.error(request, "Invalid form submission")
            return self.get(request)

        try:
            parser = LocalscanParser(request.POST['localscan'])
            parser.parse()
        except LocalscanParseException as ex:
            messages.error(request, str(ex))
            return self.get(request)

        return redirect("localscan:view", key=parser.scan.key)


class LocalscanView(View):
    """View a localscan"""
    def get(self, request, key):
        scan = get_object_or_404(Localscan, key=key)
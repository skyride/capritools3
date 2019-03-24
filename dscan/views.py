from django.contrib import messages
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect

from .exceptions import DscanParseException
from .models import Dscan
from .utils import DscanParser


class DscanSubmit(View):
    """Submit a new dscan"""
    def get(self, request):
        return render(request, "dscan/submit.html")


    def post(self, request):
        if 'dscan' not in request.POST:
            messages.error(request, "Invalid form submission")
            return self.get(request)

        try:
            parser = DscanParser(request.POST['dscan'])
            accepted, rejected = parser.parse()
        except DscanParseException as ex:
            messages.error(request, str(ex))
            return self.get(request)

        return redirect("dscan:view", key=parser.dscan.key)


def view(request, key):
    dscan = get_object_or_404(Dscan, key=key)
from django.contrib import messages
from django.db.models import Count
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect

from core.models import Alliance, Corporation, Character
from sde.models import Faction

from .exceptions import LocalscanParseException
from .models import Localscan, LocalscanItem
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

        context = {
            'scan': scan,
            'pilot_count': scan.items.count(),
            'factions': Faction.objects.filter(localscan_items__scan=scan).annotate(
                pilots=Count('localscan_items')).order_by('-pilots'),
            'alliances': Alliance.objects.filter(localscan_items__scan=scan).annotate(
                pilots=Count('localscan_items')).order_by('-pilots'),
            'corporations': Corporation.objects.filter(localscan_items__scan=scan).annotate(
                pilots=Count('localscan_items')).order_by('-pilots')
        }
        return render(request, "localscan/view.html", context)
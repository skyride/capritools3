from django.contrib import messages
from django.db.models import Count, Sum
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect

from core.models import Alliance, Corporation, Character
from sde.models import Faction

from .exceptions import LocalscanParseException
from .models import Localscan, LocalscanItem, Coalition
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
            'show_factions_bar': self.show_factions_bar(scan),
            'factions': list(self.get_factions(scan)),
            'alliances': list(self.get_alliances(scan)),
            'corporations': list(self.get_corporations(scan)),
            'coalitions': list(self.get_coalitions(scan)),
        }
        return render(request, "localscan/view.html", context)


    def get_factions(self, scan):
        return Faction.objects.filter(localscan_items__scan=scan).annotate(
            pilots=Count('localscan_items')).order_by('-pilots', 'name')

    def show_factions_bar(self, scan):
        """Only show factions bar if they account for 20% of the pilots"""
        pilots = sum(faction.pilots for faction in self.get_factions(scan))
        return (100.0 / scan.items.count()) * pilots > 20


    def get_alliances(self, scan):
        for alliance in self._get_alliances(scan):
            first = LocalscanItem.objects.filter(scan=scan, alliance=alliance, coalition__isnull=False).first()
            if first is not None:
                yield first.coalition.id, first.coalition.colour, alliance
            else:
                yield None, None, alliance

    def _get_alliances(self, scan):
        return Alliance.objects.filter(localscan_items__scan=scan).annotate(
            pilots=Count('localscan_items')
        ).order_by('-pilots', 'localscan_items__coalition__name', 'name')


    def get_corporations(self, scan):
        for corporation in self._get_corporations(scan):
            first = LocalscanItem.objects.filter(scan=scan, corporation=corporation, coalition__isnull=False).first()
            if first is not None:
                yield first.coalition.id, first.coalition.colour, corporation
            else:
                yield None, None, corporation

    def _get_corporations(self, scan):
        return Corporation.objects.filter(localscan_items__scan=scan).annotate(
            pilots=Count('localscan_items')).order_by('-pilots', 'localscan_items__coalition__name', 'name')


    def get_coalitions(self, scan):
        return Coalition.objects.filter(scan=scan).annotate(
            pilots=Count('items')).order_by('-pilots', 'name')
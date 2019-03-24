from django.contrib import messages
from django.db.models import Count
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect

from sde.models import Type, Group

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


class DscanView(View):
    """View a dscan"""
    supers = [30, 659]
    caps = [883, 547, 485, 1538, 513, 902]

    def get(self, request, key):
        dscan = get_object_or_404(Dscan, key=key)

        context = {
            'dscan': dscan,
            'ships': self.get_ships(dscan),
            'subcaps': self.get_subcaps(dscan),
            'caps': self.get_caps(dscan)
        }
        return render(request, "dscan/view.html", context)


    def get_ships(self, dscan):
        return Type.objects.filter(
            dscan_objects__scan=dscan,
            group__category_id=6,
            ).annotate(
                count=Count('dscan_objects')
            ).order_by('-count', 'name')


    def get_subcaps(self, dscan):
        return Group.objects.filter(
            types__dscan_objects__scan=dscan,
            category_id=6
        ).exclude(
            id__in=self.supers + self.caps
        ).annotate(
            count=Count('types__dscan_objects')
        ).order_by('-count', 'name')


    def get_caps(self, dscan):
        return Group.objects.filter(
            types__dscan_objects__scan=dscan,
            category_id=6,
            id__in=self.supers + self.caps
        ).annotate(
            count=Count('types__dscan_objects')
        ).order_by('-count', 'name')
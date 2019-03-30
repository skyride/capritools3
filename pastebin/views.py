from django.shortcuts import render
from django.views import View


class Submit(View):
    def get(self, request):
        return render(request, "pastebin/submit.html")
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils.timezone import now

from .forms import PasteForm, PasswordForm
from .models import Paste


class Submit(View):
    def get(self, request, form=None):
        if form is None:
            form = PasteForm()
        
        context = {
            'form': form
        }
        return render(request, "pastebin/submit.html", context)

    
    def post(self, request):
        form = PasteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("pastebin:view", key=form.instance.key)
        return self.get(request, form)


class PasteView(View):
    def get(self, request, key, password=False):
        paste = get_object_or_404(Paste, key=key)

        if paste.expires is not None and paste.expires < now():
            raise Http404

        if paste.password and not password:
            return render(request, "pastebin/password.html", {'form': PasswordForm(paste=paste)})

        return render(request, "pastebin/view.html", {'paste': paste})


    def post(self, request, key):
        paste = get_object_or_404(Paste, key=key)

        form = PasswordForm(request.POST, paste=paste)
        if form.is_valid():
            return self.get(request, key, password=True)

        return render(request, "pastebin/password.html", {'form': form})
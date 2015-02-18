from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


class LoginRequiredMixin(object):
    """Ensures that user must be authenticated in order to access view."""
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class Home(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")

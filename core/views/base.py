"""Base views and view utilities."""
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


class LoginRequiredMixin(object):

    """Ensures that user must be authenticated in order to access view."""

    @classmethod
    def as_view(cls, **initkwargs):
        """Make views that inherit this require login."""
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class Home(View):

    """Default index page handler."""

    def get(self, request, *args, **kwargs):
        """Simply render the index page."""
        return render(request, "index.html")

from django.views.generic import View
from django.http import HttpResponse


class Home(View):
    def get(self, *args):
        return HttpResponse('<html><body>Test</body></html>')

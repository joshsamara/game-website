from django.views.generic import View
from django.http import HttpResponse


class Home(View):
    def get(self, *args):
        html = """
        <html>
            <body>
                <h1>Home</h1>
                <a href="/admin">Admin page</a>
            </body>
        </html>"""
        return HttpResponse(html)

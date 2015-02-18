from django.conf.urls import include, url
from django.contrib import admin
from game_website.views import Home

urlpatterns = [
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', Home.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
]

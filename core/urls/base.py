from django.conf.urls import include, url
from django.contrib import admin
from core.views import Home, register

# Use this file to import all other url
urlpatterns = [
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', Home.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^register/$', register),

]

from django.conf.urls import include, url
from django.contrib import admin
from core.views import Home, register

# Use this file to import all other url
urlpatterns = [
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    #need Login
    url(r'^$', Home.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^register/$', register),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name' : 'registration/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

]

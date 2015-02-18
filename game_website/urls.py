from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    #need to redirect the sign in to an actual page using the next field
    url(r'^$', include('core.urls.base', namespace="core")),
    url(r'^core/', include('core.urls.base', namespace="core")),
    url(r'^admin/', include(admin.site.urls)),
]

from django.conf.urls import patterns, url
from core.views import ProfileRedirectView, ProfileView, users, notifications
from core.forms import CustomPasswordChangeForm

urlpatterns = patterns(
    '',
    url(r'^$', ProfileRedirectView.as_view(), name='base'),
    url(r'^(?P<pk>\d+)/$', ProfileView.as_view(), name='user-profile'),
    url(r'^edit/$', users.edit, name='edit'),
    url(r'^change_password/$', 'django.contrib.auth.views.password_change',
        {
            'template_name': 'registration/change_password.html',
            'password_change_form': CustomPasswordChangeForm,
            'current_app': 'core:profile',
            'post_change_redirect': 'core:profile:base'
        },
        name='password_change'),
    url(r'^notifications/(?P<notification_id>\d+)/$', notifications.base, name='notifications')
)

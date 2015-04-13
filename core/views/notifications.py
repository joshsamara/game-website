from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from core.models import UserNotification


@login_required
def base(request, notification_id):
    """URL that marks the notification read then redirects"""
    notification = UserNotification.objects.get(pk=notification_id)
    if notification.user.pk is not request.user.pk:
        response = HttpResponse(403)
    else:
        response = HttpResponseRedirect(notification.redirect_url)
        notification.read = True
        notification.save()
    return response
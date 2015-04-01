from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def post_comment_form_target():
    """
    Get the target URL for the comment form.

    Example::

        <form action="{% post_comment_form_target %}" method="post">
    """
    return reverse('game_comments:post')
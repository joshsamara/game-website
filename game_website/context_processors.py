def get_navbar_active(request):
    """ Get the first part of the current URL. """
    parts = request.path.split('/')
    return parts[1] or 'home'


def default_context_processor(request):
    """ Get context we want on every page. """
    try:
        user = request.user,
    except AttributeError:
        user = None
    context = {
        'current_user': user,
        'navbar_active': get_navbar_active(request),
    }
    return context

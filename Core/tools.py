import secrets

from django.contrib.sessions.models import Session

from .models import Link


def get_session(request):
    if request.session.session_key is None:
        request.session.save()
    session_key = request.session.session_key
    return Session.objects.get(session_key=session_key)


def get_unique_val(value):
    is_unique = False
    while not is_unique:
        value = secrets.token_urlsafe(nbytes=5)
        if not Link.objects.filter(subpart=value):
            is_unique = True
    return value

import secrets

import redis
from django.contrib.sessions.models import Session

from ShortLinks.settings import REDIS_EX
from .models import Link

client = redis.Redis(host='127.0.0.1', port=6379)


def get_session(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    return Session.objects.get(session_key=session_key)


def get_unique_val(value):
    is_unique = False
    while not is_unique:
        value = secrets.token_urlsafe(nbytes=5)
        if not Link.objects.filter(subpart=value):
            is_unique = True
    return value


def create_rule(request, main_part, subpart):
    if subpart == '':
        subpart = get_unique_val(subpart)
    session = get_session(request)
    Link.objects.create(main_part=main_part, subpart=subpart, session=session)

    client.set(subpart, main_part, ex=REDIS_EX)

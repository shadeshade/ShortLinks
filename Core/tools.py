import logging
import secrets

import redis
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404

from ShortLinks.settings import REDIS_EX
from .models import Link


logger = logging.getLogger(__name__)
redis_client = redis.Redis(host='redis', port='6379')


def get_session(request):
    if not request.session.session_key:
        request.session.create()  # new session
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
    Link.objects.create(main_part=main_part, subpart=subpart, session=session)  # create new rule


def get_redirect_url(subpart):
    try:
        link = redis_client.get(subpart)
        if link:
            link = link.decode()
        else:
            link = get_object_or_404(Link, subpart=subpart)
            redis_client.set(subpart, link.main_part, ex=REDIS_EX)
            link = link.main_part
    except redis.exceptions.ConnectionError as error:
        logger.error(error)
        link = get_object_or_404(Link, subpart=subpart)
        link = link.main_part
    return link

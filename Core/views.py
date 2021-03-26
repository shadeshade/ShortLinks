import secrets

import redis
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, RedirectView

from .forms import LinkCreate
from .models import Link

client = redis.Redis(host='127.0.0.1', port=6379)


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


class Home(ListView):
    model = Link
    form = LinkCreate
    paginate_by = 10

    def get_queryset(self):
        session = get_session(self.request)
        queryset = Link.objects.filter(session=session).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, **kwargs):
        form = LinkCreate(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            self.object_list = self.get_queryset()
            context = self.get_context_data()

            context['main_part'] = data.get('main_part')
            context['subpart'] = data.get('subpart')

            if context['subpart'] == '':
                context['subpart'] = get_unique_val(context['subpart'])

            session = get_session(request)
            new_link = Link.objects.create(main_part=context['main_part'], subpart=context['subpart'],
                                           session=session)
            new_link.save()
            client.set(context['subpart'], context['main_part'], ex=600)

            return super(Home, self).render_to_response(context)
        else:
            messages.error(request=request, message='Input unique subpart, please')
            return redirect(reverse('home_page'))


class LinkRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if client.get(kwargs['short_link']):
            link = client.get(kwargs['short_link'])
        else:
            link = get_object_or_404(Link, subpart=kwargs['short_link'])
            link = link.main_part
        return link

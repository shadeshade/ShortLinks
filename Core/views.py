from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.sessions.models import Session

from .forms import LinkCreate
from .models import Link
import secrets


class Home(ListView):
    model = Link
    queryset = Link.objects.all()
    form = LinkCreate

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_list = self.get_queryset()

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, **kwargs):
        form = LinkCreate(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            context = self.get_context_data()

            context['main_part'] = data.get('main_part')
            context['subpart'] = data.get('subpart')

            if context['subpart'] == '':
                context['subpart'] = get_unique_val(context['subpart'])

            session = get_session(request)
            new_link = Link.objects.create(main_part=context['main_part'], subpart=context['subpart'],
                                           session=session)
            new_link.save()
            return super(Home, self).render_to_response(context)
        else:
            messages.error(request=request, message='Input unique subpart, please')
            return redirect(reverse('home_page'))


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

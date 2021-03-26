from django.urls import path

from .views import Home, LinkRedirectView

urlpatterns = [
    path('', Home.as_view(), name='home_page'),
    path('r/<str:short_link>/', LinkRedirectView.as_view(), name='link_redirect_view')
]

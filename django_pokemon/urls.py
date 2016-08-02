"""django_pokemon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include
from pokemonbot.views import *

admin.autodiscover()

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',StartView.as_view(),name='start'),
    url(r'^create_user$',CreateView.as_view(),name='create'),
    url(r'^settings/(?P<id>\d+)/$',SettingsView.as_view(),name='settings'),
    url(r'^bot/(?P<id>\d+)/$',BotView.as_view(),name='bot'),
    url(r'^ajax$',AjaxView.as_view(),name='ajax'),
    url(r'^logout/$','pokemonbot.views.logout', name='logout')
]
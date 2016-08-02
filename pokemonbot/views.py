from django.contrib import auth
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse
from .forms import *
from .models import *
from PokemonGo.pokecli import init_config
from PokemonGo.pokemongo_bot import PokemonGoBot


class StartView(FormView):
    form_class = LoginForm
    template_name = 'start.html'

    def form_valid(self, form):
        fcd = form.cleaned_data
        user=auth.authenticate(username=fcd['username'], password=fcd['password'])
        if user is not None:
            if user.is_active:
                auth.login(self.request, user)
                return redirect('settings', id=self.request.user.id)


class CreateView(FormView):
    form_class = UserCreateForm
    template_name = 'create.html'

    def form_valid(self, form):
        user = form.save()
        fcd = form.cleaned_data
        user=auth.authenticate(username=fcd['username'], password=fcd['password1'])
        if user is not None:
            if user.is_active:
                auth.login(self.request, user)
                return redirect('settings', id=self.request.user.id)


class SettingsView(LoginRequiredMixin,FormView):
    form_class = SettingsForm
    template_name = 'settings.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.id==int(self.kwargs['id']):
            return super(SettingsView, self).dispatch(*args, **kwargs)
            #return super(self.__class__, self).dispatch(*args, **kwargs) check this
        else:
            return redirect('start')

    def form_valid(self, form):
        fcd = form.cleaned_data
        UserSettings.objects.create(
                                    user=self.request.user,
                                    google_email=fcd['google_email'],
                                    google_password=fcd['google_password'],
                                    location_lon=fcd['location_lon'],
                                    location_lat=fcd['location_lat'],
                                    gmapkey=fcd['gmapkey'])
        return redirect('bot', id=self.request.user.id)


class AjaxView(LoginRequiredMixin,TemplateView):
    template_name = 'ajax.html'

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(AjaxView, self).dispatch(*args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     try:
    #         self.request.user.usersettings
    #         return render(request, self.template_name)
    #     except Exception, e:
    #         return render(request, self.template_name, {'error': ' Please, add info in\
    #                                                              your settings'})

    # @staticmethod
    # def success_info(curr_request):
    #     return JsonResponse({'start_success': 'Your bot is running'})

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            http_post=request.POST
            start=http_post.get('start',False)
            stop=http_post.get('stop',False)
            if start:
                user_settings=self.request.user.usersettings
                curr_location=','.join([str(user_settings.location_lon),
                                        str(user_settings.location_lat)])
                config =init_config(username=user_settings.google_email,
                                    password=user_settings.google_password,
                                    location=curr_location,
                                    gmapkey=user_settings.gmapkey)

                bot = PokemonGoBot(config)
                bot.start()
                #return JsonResponse({'start_success': 'Your bot is running'})
                while True:
                    bot.take_step()
                if stop:
                    bot.stop()
                    return JsonResponse({'stop_success': 'Your bot is stopped'})



class BotView(LoginRequiredMixin,TemplateView):
    template_name = 'bot.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.id==int(self.kwargs['id']):
            return super(BotView, self).dispatch(*args, **kwargs)
            #return super(self.__class__, self).dispatch(*args, **kwargs)
        else:
            return redirect('start')


def logout(request):
    auth.logout(request)
    return redirect('start')
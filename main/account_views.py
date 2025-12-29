from django.contrib.auth.views import LoginView as DjangoLoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from .forms import MyUserCreationForm
from site_conf.models import SiteConfig

class LoginView(DjangoLoginView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().get(request, *args, **kwargs)


class SignUpView(CreateView):
    form_class = MyUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        config = SiteConfig.get_current()
        if not config or not config.can_signup:
            messages.error(request, 'Регистрация новых пользователей временно отключена администратором.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().get(request, *args, **kwargs)
    

def logout_view(request):
    logout(request)
    return redirect('index')
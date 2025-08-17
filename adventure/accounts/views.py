from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from adventure.accounts.forms import AppUserCreationForm, ProfileForm
from adventure.accounts.models import AppProfile

UserModel = get_user_model()


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class RegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = "registration/register.html"

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)

        return response


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = AppProfile
    form_class = ProfileForm
    template_name = "registration/profile.html"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('home')

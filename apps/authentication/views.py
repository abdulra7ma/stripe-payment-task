from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView

from .forms import LoginForm, SignupForm


class LoginView(FormView):
    template_name = "authentication/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("school:school-index")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("school:school-index")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.auth_user
        login(self.request, user)
        return super().form_valid(form)

class SignupView(FormView):
    template_name = "authentication/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("auth:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("school:school-index")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save(True)
        return super().form_valid(form)



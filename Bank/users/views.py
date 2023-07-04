from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib import messages
from .forms import UserRegistrationForm
from django.views.generic import FormView

class RegisterView(FormView):
    form_class = UserRegistrationForm
    template_name = "register.html"
    success_url = reverse_lazy("login")


    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Account Created Successfully! You can now sign in!")
        form.save()
        return super().form_valid(form)


def logoutView(request):
    logout(request)
    return redirect("home")


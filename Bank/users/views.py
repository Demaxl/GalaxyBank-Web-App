import json
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .forms import UserRegistrationForm, ProfileUpdateForm
from django.views.generic import FormView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from pprint import pprint

class RegisterView(FormView):
    form_class = UserRegistrationForm
    template_name = "register.html"
    success_url = reverse_lazy("login")


    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Account created successfully! You can now sign in!")
        form.save()
        return super().form_valid(form)

class ProfileView(LoginRequiredMixin, UserPassesTestMixin, DetailView, FormView):
    model = User
    template_name = "profile.html"
    context_object_name = "user"
    form_class = ProfileUpdateForm

    def test_func(self):
        return self.request.user.username == self.kwargs["username"] 
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect("home")
        return super().handle_no_permission()

    def get_object(self, queryset=None):
        username = self.kwargs["username"]
        return self.model.objects.get(username=username)
    
    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = User.objects.get(username=self.request.user.username)
        
        if user.profile.pin != data.get("oldPin"):
            return JsonResponse({"error":"Incorrect PIN"}, status=401)
        
        user.profile.pin = data.get("newPin")
        user.profile.save()
        return HttpResponse(status=204)
    
    def post(self, request, *args, **kwargs):
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Account info updated")
        return HttpResponseRedirect(request.path)

def logoutView(request):
    logout(request)
    return redirect("home")


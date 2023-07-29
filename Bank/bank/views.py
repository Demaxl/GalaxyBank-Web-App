from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(View):
    def get(self, request):
        return render(request, "home.html", {
            "active_page": "home"
        })

class DepositView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "deposit.html")
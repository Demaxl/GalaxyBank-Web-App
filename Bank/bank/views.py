from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal

from .models import Transaction
from pprint import pprint

class HomePageView(View):
    def get(self, request):
        return render(request, "home.html", {
            "active_page": "home"
        })

class DepositView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "deposit.html")
    
    def post(self, request):
        user = request.user
        amount = request.POST['amount']
        pin = request.POST['pin']

        if user.profile.pin != pin:
            messages.error(request, "Invalid transaction pin")
            return redirect("deposit")

        else:
            tr = Transaction.objects.create(type="deposit", amount=Decimal(amount), user=user)
            messages.success(request, f"You have successfully deposited ${amount}")

        return redirect("home")
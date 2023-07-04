from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout

def logoutView(request):
    logout(request)
    return redirect("home")

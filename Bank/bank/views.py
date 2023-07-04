from django.shortcuts import render
from django.http import HttpResponse 
from django.views.generic import View
from django.contrib import messages


class HomePageView(View):
    def get(self, request):
        return render(request, "home.html", {
            "active_page": "home"
        })
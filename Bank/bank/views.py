from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import View, ListView, DetailView
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.db.models import Q

from .models import Transaction
from pprint import pprint

class HomePageView(LoginRequiredMixin, View):
    def get(self, request):
        context = {}

        user = request.user        
        if user.is_authenticated:
            transactions = Transaction.objects.filter(Q(user=user) | Q(receiver=user)).order_by("-time")[:3]
            context["received_transactions"] = user.received_transactions.all()
            context["transactions"] = transactions

        return render(request, "home.html", context)

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
            messages.success(request, f"You have successfully deposited ${amount} into your account")

        return redirect("home")
    
class WithdrawView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "withdraw.html")
    
    def post(self, request):
        user = request.user
        amount = request.POST['amount']
        pin = request.POST['pin']

        if user.profile.pin != pin:
            messages.error(request, "Invalid transaction pin")
            return redirect("withdraw")

        else:
            try:
                tr = Transaction.objects.create(type="withdraw", amount=Decimal(amount), user=user)
            except ValidationError as err:
                messages.error(request, "<strong>Insufficient funds!</strong> Your transaction could not be processed due to insufficient funds in your account")
                return redirect("withdraw")
            
            messages.success(request, f"You have successfully withdrawn ${amount} from your account")

        return redirect("home")
    
class TransferView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "transfer.html")
    
    def post(self, request):
        user = request.user
        amount = request.POST['amount']
        pin = request.POST['pin']
        receiver = User.objects.get(username=request.POST['receiver'])

        if user.profile.pin != pin:
            messages.error(request, "Invalid transaction pin")
            return redirect("transfer")
    
        try:
            tr = Transaction.objects.create(type="transfer", amount=Decimal(amount), user=user, receiver=receiver)
        except ValidationError as err:
            messages.error(request, "<strong>Insufficient funds!</strong> Your transaction could not be processed due to insufficient funds in your account")
            return redirect("transfer")
        
        messages.success(request, f"You have successfully transfer ${amount} to {receiver.username}")
        return redirect("home")
    
class TransactionsListView(LoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = "transactions"
    ordering = ["-time"]
    template_name = "transactions_history.html"

    paginate_by = 3

    def get_queryset(self):
        return Transaction.objects.filter(Q(user=self.request.user) | Q(receiver=self.request.user)).order_by("-time")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['received_transactions'] = self.request.user.received_transactions.all()

        return context

class TransactionsDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Transaction
    context_object_name = "transaction"
    template_name = "transactions_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['received_transactions'] = self.request.user.received_transactions.all()

        return context

    def test_func(self) -> bool | None:
        transaction = self.get_object()
        return (self.request.user == transaction.user ) or (self.request.user == transaction.receiver)

class API:
    @staticmethod
    def suggest(request):
        input_user = request.GET.get("user")
        current_user = request.GET.get("requestUser")

        suggested_users = User.objects.filter(username__icontains=input_user).exclude(username=current_user)

        data = {}
        for user in suggested_users:
            data[user.username] = [user.profile.first_name + " " + user.profile.last_name, user.profile.image.url]

        return JsonResponse(data)


from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("deposit", "Deposit"),
        ("withdraw", "Withdrawal"),
        ("transfer", "Transfer")
    ]
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, default="transfer")
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    user = models.ForeignKey(User, on_delete=models.SET("Deleted User"), related_name="transactions")
    
    def __str__(self):
        return f"{self.type} by {self.user}"
    
class Transfer(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, primary_key=True, related_name="transfer")
    receiver = models.ForeignKey(User, on_delete=models.SET("Deleted User"), related_name="received_transactions", null=True)



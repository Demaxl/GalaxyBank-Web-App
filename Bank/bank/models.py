from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



class Transaction(models.Model):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER = "transfer"
    TRANSACTION_TYPES = [
        (DEPOSIT, "Deposit"),
        (WITHDRAW, "Withdrawal"),
        (TRANSFER, "Transfer")
    ]
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, default=TRANSFER)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    user = models.ForeignKey(User, on_delete=models.SET("Deleted User"), related_name="transactions")
    receiver = models.ForeignKey(User, on_delete=(models.SET("Deleted User")), related_name="received_transaction", blank=True, null=True)

    def __str__(self):
        return f"{self.type} by {self.user}"
    
    def save(self, *args, **kwargs):
        self.full_clean()

        if self.type == self.DEPOSIT:
            self.user.profile.balance += self.amount
            self.user.profile.save()

        elif self.type == self.WITHDRAW:
            self.user.profile.balance -= self.amount
            self.user.profile.save()
        
        return super().save(*args, **kwargs)
        

    def clean(self):
        if self.type == self.TRANSFER and not self.receiver:
            raise ValidationError(
                {"receiver": _("A receiver must be specified for transfers")})


        if (self.type != self.DEPOSIT) and (self.amount > self.user.profile.balance):
            raise ValidationError(
                {"amount": _("Insufficient funds in user account")}
            )

   

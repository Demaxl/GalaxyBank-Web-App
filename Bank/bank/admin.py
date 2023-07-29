from django.contrib import admin
from .models import Transaction, Transfer

class TransferInline(admin.StackedInline):  # You can use TabularInline for a more compact display.
    model = Transfer

class TransactionAdmin(admin.ModelAdmin):
    inlines = [TransferInline]

admin.site.register(Transaction, TransactionAdmin)
# admin.site.register(Transaction)
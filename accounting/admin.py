from django.contrib import admin

from .models import Transaction, BankAccount, TransactionSubject


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'pk', 'description', 'amount_pay', 'amount_rec', 'account_level', 'created', 'subject',
    ]
    list_filter = ['amount_pay', 'amount_rec']
    search_fields = ['description', 'amount_pay', 'amount_rec', 'subject__title', 'bank_account__title']
    # list_editable = ['active',]


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'current_level', 'initial_level', 'bank_name', 'card_number', 
    ]


@admin.register(TransactionSubject)
class TransactionSubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'transaction_kind', ]
    # list_editable = ['title',  ]
    # list_display_links = ['title',]
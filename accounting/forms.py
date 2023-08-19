from django import forms

from .models import Transaction, BankAccount, TransactionSubject


class PayForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.fields['subject'].queryset = TransactionSubject.objects.filter(transaction_kind='pay')
        self.fields['description'].required = True
        self.fields['bank_account'].required = True
    class Meta:
        model = Transaction
        fields = [
            'amount_pay', 'description', 'subject', 'bank_account', # 'date', 'receipt_image', 'receipt_file'
        ]
        widgets = {
            'amount_pay': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }

class RecForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.fields['subject'].queryset = TransactionSubject.objects.filter(transaction_kind='rec')
        self.fields['description'].required = True
        self.fields['bank_account'].required = True
    class Meta:
        model = Transaction
        fields = [
            'amount_rec', 'description', 'subject', 'bank_account', #'date', 'receipt_image', 'receipt_file'
        ]
        widgets = {
            'amount_rec': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }



PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 5)]

class DateForm(forms.Form):
    day = forms.TypedChoiceField(
        choices=[(i, str(i)) for i in range(1, 32)],
        coerce=int,
        label=''
    )
    month = forms.TypedChoiceField(
        choices=[(i, str(i)) for i in range(1, 13)],
        coerce=int,
        label=''
    )
    year = forms.TypedChoiceField(
        choices=[(i, str(i)) for i in range(2023, 2024)],
        coerce=int,
        label=''
    )
    
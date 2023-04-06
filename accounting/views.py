from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView

from .models import Transaction, BankAccount, TransactionSubject
from .forms import PayForm, RecForm


@staff_member_required
def AccountingDashboardView(request):
    context = {}
    context["object_list"] = Transaction.active_trans.all().select_related('bank_account', 'subject')
    context["page_title"] = _('Accounting dashboard')
    context["mainNavSection"] = 'accounting'
    return render(
        request, 
        'accounting/dashboard.html',
        context
    )

class TransactionsListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'accounting/transactions_list.html'
    queryset = Transaction.active_trans.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Transactions')
        context['mainNavSection'] = 'accounting' 
        context['accSection'] = 'transaction' 
        return context


class TransactionSubjectsListView(LoginRequiredMixin, ListView):
    model = TransactionSubject
    template_name = 'accounting/transaction_subjects_list.html'
    queryset = TransactionSubject.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Transaction subjects')
        context['mainNavSection'] = 'accounting'
        context['accSection'] = 'subject' 
        return context


class BankAccountListView(LoginRequiredMixin, ListView):
    model = BankAccount
    template_name = 'accounting/bank_accounts_list.html'
    queryset = BankAccount.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Bank accounts')
        context['mainNavSection'] = 'accounting'
        context['accSection'] = 'bank' 
        return context


class AddPayment(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = PayForm
    template_name = 'accounting/add_payment.html'

    def get_success_url(self):
        return reverse ('accounting:accounting_dashboard')
    
    def form_valid(self, form):
        # form.instance.bank_account.current_level -= form.instance.amount_pay   
        form.instance.account_level = form.instance.bank_account.current_level - form.instance.amount_pay
        form.instance.bank_account.current_level = form.instance.account_level
        form.instance.bank_account.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Add payment')
        context['mainNavSection'] = 'accounting'
        context['accSection'] = 'pay' 
        return context


class AddRecieve(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = RecForm
    template_name = 'accounting/add_payment.html'

    def get_success_url(self):
        return reverse ('accounting:transactions_list')
    
    def form_valid(self, form):        
        form.instance.account_level = form.instance.bank_account.current_level + form.instance.amount_rec
        form.instance.bank_account.current_level = form.instance.account_level
        form.instance.bank_account.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Add recieve')
        context['mainNavSection'] = 'accounting'
        context['accSection'] = 'rec' 
        return context


class AddTransactionSubject(LoginRequiredMixin, CreateView):
    model = TransactionSubject
    fields = ['title', 'transaction_kind']
    template_name = 'accounting/add_payment.html'

    def get_success_url(self):
        return reverse ('accounting:transaction_subjects_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Add transaction subject')
        context['mainNavSection'] = 'accounting'
        context['accSection'] = 'subject' 
        return context


class UpdateTransactionSubject(LoginRequiredMixin, UpdateView):
    model = TransactionSubject
    fields = ['title', 'transaction_kind']
    template_name = 'accounting/add_payment.html'

    def get_success_url(self):
        return reverse ('accounting:transaction_subjects_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Update transaction subject')
        context['mainNavSection'] = 'accounting' 
        context['accSection'] = 'subject' 
        return context
    

def RemoveTransactionView(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)    
    if transaction.bank_account:
        transaction.bank_account.current_level = transaction.bank_account.current_level + transaction.amount_pay - transaction.amount_rec
        transaction.bank_account.save()
    transaction.active = False
    transaction.save()
    return redirect(request.META['HTTP_REFERER'])
# from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
# from django.utils import timezone
from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView
from django.db.models import Sum
from .models import Transaction, BankAccount, TransactionSubject
from .forms import PayForm, RecForm, DateForm


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
    form_class = DateForm
    queryset = Transaction.active_trans.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Transactions')
        context['mainNavSection'] = 'accounting' 
        context['accSection'] = 'transaction'
        context['from_date'] = DateForm(auto_id="from_%s", prefix='from')
        context['to_date'] = DateForm(auto_id="to_%s", prefix='to')
        context['pay_sum'] = self.get_queryset().aggregate(sum=Sum('amount_pay'))['sum']
        context['rec_sum'] = self.get_queryset().aggregate(sum=Sum('amount_rec'))['sum']

        context["from_day"] = int(self.request.GET.get('from-day', '1'))
        context["from_month"] = int(self.request.GET.get('from-month', '1'))
        context["from_year"] = int(self.request.GET.get('from-year', '2023'))
        context["to_day"] = int(self.request.GET.get('to-day', '1'))
        context["to_month"] = int(self.request.GET.get('to-month', '1'))
        context["to_year"] = int(self.request.GET.get('to-year', '2023'))
        
        from_date = datetime(context["from_year"], context["from_month"], context["from_day"])
        to_date = datetime(context["to_year"], context["to_month"], context["to_day"])
        if from_date == datetime(2023, 1, 1) and to_date == datetime(2023, 1, 1):
            context['from_date_date'] = None 
            context['to_date_date'] = None 
        else:
            context['from_date_date'] = from_date 
            context['to_date_date'] = to_date
            # TODO: these two lines does not work to initial form of date
            context['from_date'] = DateForm(auto_id="from_%s", prefix='from', initial={'from-day': context["from_day"], 'from-month': context["from_month"], 'from-year': context["from_year"]})
            context['to_date'] = DateForm(auto_id="to_%s", prefix='to', initial={'to-day': context["to_day"], 'to-month': context["to_month"], 'to-year': context["to_year"]})
            
        
        link_temp = "?from-day={}&from-month={}&from-year={}&to-day={}&to-month={}&to-year={}"
        context['monthes'] = [
            {'name': _('Farvardin'), 
            'link': link_temp.format('21', '3', '2023', '20', '4', '2023')},
            {'name': _('Ordibehesht'), 
            'link': link_temp.format('21', '4', '2023', '21', '5', '2023')},
            {'name': _('Khordad'), 
            'link': link_temp.format('22', '5', '2023', '21', '6', '2023')},
            {'name': _('Tir'), 
            'link': link_temp.format('22', '6', '2023', '22', '7', '2023')},
            {'name': _('Mordad'), 
            'link': link_temp.format('23', '7', '2023', '22', '8', '2023')},
            {'name': _('Shahrivar'), 
            'link': link_temp.format('23', '8', '2023', '22', '9', '2023')},
        ]
        
        if self.kwargs.get('subject'):
            context["subject"] = self.kwargs.get('subject')
        else:
            context["subject"] = 'all'

        

        if self.kwargs.get('bank'):
            context["bank"] = self.kwargs.get('bank')
        else:
            context["bank"] = 'all'
        

        if self.request.GET.get('search'):
            context["search"] =  self.request.GET.get('search')

        return context
    
    def get_queryset(self):
        from_day= None
        queryset =  super().get_queryset()
        
        if self.request.GET.get('from-day'):
            from_day = int(self.request.GET.get('from-day'))
            to_day = int(self.request.GET.get('to-day'))
            from_month = int(self.request.GET.get('from-month'))
            to_month = int(self.request.GET.get('to-month'))
            from_year = int(self.request.GET.get('from-year'))
            to_year = int(self.request.GET.get('to-year'))


        if from_day:
            from_date = datetime(from_year, from_month, from_day)
            to_date = datetime(to_year, to_month, to_day)
            # print(from_date, to_date)
            try:
                queryset = queryset.filter(created__range=(from_date, to_date))
                # print('hi')
            except:
                pass
        
        if self.kwargs.get('subject'):
            subject = self.kwargs.get('subject')
            subjects = TransactionSubject.objects.all().values_list('title', flat=True)
            if subject == 'all':
                queryset = queryset.filter(subject__title__in=subjects)                
            else:
                queryset = queryset.filter(subject__title=subject)
        
        if self.kwargs.get('bank'):
            bank = self.kwargs.get('bank')
            banks = BankAccount.objects.values_list('title', flat=True)
            if bank == 'all':
                queryset = queryset.filter(bank_account__title__in=banks)
            else:
                queryset = queryset.filter(bank_account__title=bank)            
        
        if self.request.GET.get('search'):
            search =  self.request.GET.get('search')
            queryset = queryset.filter(description__icontains=search)
        
        return queryset    

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
    return redirect('accounting:accounting_dashboard')
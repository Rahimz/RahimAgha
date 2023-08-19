from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'accounting'

urlpatterns = [
    path('', views.AccountingDashboardView, name="accounting_dashboard"),
    path('transactions/', views.TransactionsListView.as_view(), name="transactions_list"),
    path('transactions/subject/<str:subject>/', views.TransactionsListView.as_view(), name="transactions_list_subject"),
    path('transactions/subject/<str:subject>/account/<str:bank>/', views.TransactionsListView.as_view(), name="transactions_list_subject_bank"),

    path('add-payment/', views.AddPayment.as_view(), name="add_payment"),
    path('add-receive/', views.AddRecieve.as_view(), name="add_receive"),
    path('remove-transaction/<int:pk>/', views.RemoveTransactionView, name="remove_transaction"),
    path('bank-accounts/', views.BankAccountListView.as_view(), name="bank_accounts_list"),
    path('transaction-subjects/', views.TransactionSubjectsListView.as_view(), name="transaction_subjects_list"),
    path('add-transation-subject/', views.AddTransactionSubject.as_view(), name="add_transaction_subject"),
    path('add-transation-subject/<int:pk>/', views.UpdateTransactionSubject.as_view(), name="update_transaction_subject"),
]

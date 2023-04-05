from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid 
from django.conf import settings

from quizes.models import TimeStampedModel



class BankAccount(TimeStampedModel):
    title = models.CharField(
        _('Account title'),
        max_length=150,
        unique=True,        
    )
    bank_name = models.CharField(
        max_length=50,
        null=True, 
        blank=True,
    )
    card_number = models.CharField(
        _('Card number'),
        max_length=16,
        null=True, 
        blank=True        
    )
    account_number = models.CharField(
        _('Account number'),
        max_length=20,
        null=True, 
        blank=True
    )
    BIN = models.CharField(
        'BIN',
        max_length=24,
        null=True, 
        blank=True
    )
    interest_rate = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0
    )   
    initial_level = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGIT,
        decimal_places=0, 
        default=0
    )
    current_level = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGIT,
        decimal_places=0, 
        default=0
    )

    class Meta:
        verbose_name = _('Bank account')
        verbose_name_plural = _('Bank accounts')
        ordering = ('-title', )
    
    def __str__(self):
        return self.title
    
    def get_transactions_sum(self):
        return sum(t.amount_rec - t.amount_pay for t in self.transactions.all())
    
    def save(self, *args, **kwargs):        
        self.current_level = self.initial_level - self.get_transactions_sum() 
        return super().save(*args, **kwargs) 

class TransactionSubject(TimeStampedModel):
    title = models.CharField(
        max_length=100,
        unique=True,                
    )
    # https://docs.djangoproject.com/en/4.1/ref/models/fields/#enumeration-types
    class TransactionKind(models.TextChoices):
        PAYMENT = 'pay', _('Payment')
        RECEIVE = 'rec', _('Receive')
    transaction_kind = models.CharField(
        max_length=3,
        choices=TransactionKind.choices,
        default=TransactionKind.PAYMENT,
    )

    class Meta:
        verbose_name = _('Transaction subject')
        verbose_name_plural = _('Transaction subjects')
        ordering = ('-pk', )

    def __str__(self):
        return self.title

class Transaction(TimeStampedModel):
    uuid = models.UUIDField(		
		default = uuid.uuid4,
		editable = False
    )
    amount_pay = models.DecimalField(
        _('Pay amount'),
        max_digits=settings.DEFAULT_MAX_DIGIT,
        decimal_places=0, 
        default=0
    )
    amount_rec = models.DecimalField(
        _('Receive amount'),
        max_digits=settings.DEFAULT_MAX_DIGIT,
        decimal_places=0, 
        default=0
    )
    # show the bank account at the time of transaction
    account_level = models.DecimalField(
        _('Account level'),
        max_digits=settings.DEFAULT_MAX_DIGIT,
        decimal_places=0, 
        default=0
    )
    date = models.DateTimeField(
        _('Transaction date'),
        null=True,
        blank=True
    )
    bank_account = models.ForeignKey(
        BankAccount,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='transactions'
    )
    registrar = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True
    )    
    subject = models.ForeignKey(
        TransactionSubject,
        on_delete=models.SET_NULL,                
        null=True, 
        blank=True
    )
    description = models.TextField(
        _('Description'),
        null=True, 
        blank=True
    )
    receipt_image = models.ImageField(
        _('Receipt image'),
        upload_to='accounting/receipt',
        null=True, 
        blank=True
    )
    receipt_file = models.FileField(
        _('Receipt file'),
        upload_to='accounting/receipt',
        null=True, 
        blank=True
    )

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
        ordering = ('-pk', )

    def __str__(self):
        desc = self.description if self.description else ''
        if self.amount_pay:
            return f"{str(self.amount_pay)} {desc}" 
        elif self.amount_rec:
            return f"{str(self.amount_rec)} {desc}"         
    
    def update_account_level(self):
        return self.account_level + self.bank_account.initial_level

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = self.created
        # this one should be calculated in the view not in the model
        # self.account_level = self.bank_account.current_level - self.amount_pay + self.amount_rec
        return super().save(*args, **kwargs)    
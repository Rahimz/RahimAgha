from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def AccountingDashboardView(request):
    context = {}
    context["page_title"] = _('Accounting dashboard')
    context["mainNavSection"] = 'accounting'
    return render(
        request, 
        'accounting/dashboard.html',
        context
    )

from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


def bookstore(request):
    return render(
        request,
        'bookstore/bookstore.html',
        {
            'page_title': _('Bookstore solution')
        }
    )

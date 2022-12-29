from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from .models import Feature


def bookstore(request):    
    
    return render(
        request,
        'bookstore/static_bookstore.html',
        {
            'page_title': _('Bookstore solution'),            
        }
    )


# def bookstore(request):
#     features = Feature.objects.filter(published=True)

#     return render(
#         request,
#         'bookstore/bookstore.html',
#         {
#             'page_title': _('Bookstore solution'),
#             'features': features, 
#         }
#     )

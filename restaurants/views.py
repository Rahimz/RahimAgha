from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

def ResHomeView(request):
    context = dict(
        page_title = _("Restaurants"),
    )
    return render(
        request,
        'restaurants/res_home.html',
        context
    )
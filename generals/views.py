from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


def HomeView(request):
    # if request.GET.get('SwitchNight') == 'on':
    #     print (request.GET. get('SwitchNight'))

    return render(
        request,
        'home.html',
        {
            'page_title': _('Home')
        }
    )
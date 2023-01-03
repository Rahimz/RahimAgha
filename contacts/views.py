from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
import urllib
import json
from django.conf import settings 


from .forms import ContactForm
from .models import Contact

def contacts(request):
    page_title = _('Contacts')
    require = request.GET.get('require')  if request.GET.get('require') in ('customization', 'price') else None
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''
            if result['success']:
                new_form = form.save(commit=False)
                if require:
                    new_form.require = require
                new_form.save()
                return render( 
                    request, 
                    'contacts/contacts.html',
                    {
                        'form': ContactForm(),
                        'success_message': _('Thanks a lot, Your message is registered and I will contact you'),
                        'page_title': page_title,
                        
                    })
    else:
        form = ContactForm()
    return render (
        request, 
        'contacts/contacts.html',
        {
            'form': form,
            'page_title': page_title,
            'require': require
        }
    )

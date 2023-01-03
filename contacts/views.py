from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from .forms import ContactForm
from .models import Contact

def contacts(request):
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            return render( 
                request, 
                'contacts/contacts.html',
                {
                    'form': ContactForm(),
                    'success_message': _('Thanks a lot, Your message is registered and I will contact you')
                })
    else:
        form = ContactForm()
    return render (
        request, 
        'contacts/contacts.html',
        {
            'form': form 
        }
    )

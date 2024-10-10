from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

import requests
from django.http import JsonResponse
from django.views import View

from .models import GeoRecord

def HomeView(request):
    # if request.GET.get('SwitchNight') == 'on':
    #     print (request.GET. get('SwitchNight'))

    return render(
        request,
        'home.html',
        {
            'page_title': _('Home'),
            'mainNavSection': 'home'
        }
    )




class GetCountryFromIP(View):
    def get(self, request, ip):
        # Validate the IP address format (optional, but recommended)
        if ip == '127.0.0.1':
            return 'IR'
        if not self.is_valid_ip(ip):
            return JsonResponse({'error': 'Invalid IP address'}, status=400)

        # Make a request to the ipinfo.io API
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json")
            response.raise_for_status()  # Raise an error for bad responses

            # Extract country information
            country = response.json().get('country')

            try:
                record = GeoRecord.objects.create(
                    ip=ip,
                    country=country
                )
            except:
                pass


            # Return the country in a JSON response
            return JsonResponse({'country': country})

        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

    def is_valid_ip(self, ip):
        # Simple IP validation (IPv4 and IPv6)
        import re
        # Regex for IPv4 and IPv6
        ipv4_pattern = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
        ipv6_pattern = r'^[0-9a-fA-F:]+$'
        return re.match(ipv4_pattern, ip) or re.match(ipv6_pattern, ip)
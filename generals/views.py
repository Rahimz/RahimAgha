from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

import requests
from django.http import JsonResponse
from django.views import View

from .models import GeoRecord
from core.settings.secret import API_KEY_LOCATION

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
            # print('local')
            return JsonResponse({'country': 'IR'})
        if not self.is_valid_ip(ip):
            return JsonResponse({'error': 'Invalid IP address'}, status=400)
        
        if GeoRecord.objects.filter(ip=ip).exists():
            # print('in databse')
            record = GeoRecord.objects.filter(ip=ip).latest('created')
            record.count += 1 
            record.save()
            return JsonResponse({'country': record.country}, status=200)
            
        # Make a request 
        try:
            # print('in api')
            # response = requests.get(f"https://ipinfo.io/{ip}/json")
            # country = response.json().get('country')
            
            response = requests.get(f"https://api.ip2location.io/?key={API_KEY_LOCATION}&ip={ip}")
            response.raise_for_status()  # Raise an error for bad responses

            # Extract country information
            country = response.json().get('country_code')

            try:
                record = GeoRecord.objects.create(
                    ip=ip,
                    country=country
                )
            except:
                pass


            # Return the country in a JSON response
            return JsonResponse({'country': country}, status=200)

        except requests.RequestException as e:
            # print('in api exception')
            return JsonResponse({'error': str(e)}, status=500)

    def is_valid_ip(self, ip):
        # Simple IP validation (IPv4 and IPv6)
        import re
        # Regex for IPv4 and IPv6
        ipv4_pattern = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
        ipv6_pattern = r'^[0-9a-fA-F:]+$'
        return re.match(ipv4_pattern, ip) or re.match(ipv6_pattern, ip)
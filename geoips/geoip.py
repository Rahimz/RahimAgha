
from django.conf import settings
from geoip2 import database, errors

import os

GEOIP_DATABASE_PATH = os.path.join(settings.BASE_DIR, 'geoips', 'DB',  'IP2LOCATION-LITE-DB11.MMDB')


# 2. Initialize the Reader object ONCE at the module level.
# This code runs only one time when Django starts up and imports this module.
try:
    # This 'reader' object will be kept in memory and reused for all requests.
    reader = database.Reader(GEOIP_DATABASE_PATH)
    print("Successfully loaded GeoIP2 database.")
except FileNotFoundError:
    # If the file is missing, we create a None object and handle it in the function.
    # This prevents the entire app from crashing on startup if the file is missing.
    reader = None
    print(f"GeoIP2 database not found at {GEOIP_DATABASE_PATH}. Geolocation will be disabled.")


# 3. Define your lookup function to USE the pre-loaded reader.
def GeoLocation(ip_address):
    # Check if the reader was successfully loaded on startup.
    if reader is None:
        return {'error': 'GeoIP database not loaded.'}

    location_data = {'ip': ip_address}
    try:
        # We are now using the 'reader' object that was created when the app started.
        # No more opening or closing the file here!
        response = reader.city(ip_address)

        location_data.update({
            'country_code': response.country.iso_code,
            'country_name': response.country.name,
            'state': response.subdivisions.most_specific.name if response.subdivisions else None,
            'city': response.city.name if response.city else None,
            'postal_code': response.postal.code if response.postal else None,
            'latitude': response.location.latitude,
            'longitude': response.location.longitude,
            'timezone': response.location.time_zone,
        })
    except errors.AddressNotFoundError:
        location_data['error'] = f"Location for IP address {ip_address} not found in the database."
    except Exception as e:
        location_data['error'] = str(e)

    return location_data

# Optional: Add a function to close the reader when the app shuts down, though it's often not strictly necessary.
# from django.apps import AppConfig
# 
# class YourAppConfig(AppConfig):
#     def ready(self):
#         import atexit
#         atexit.register(self.close_geoip_reader)
#
#     def close_geoip_reader(self):
#         if reader:
#             reader.close()
#             print("GeoIP2 database reader closed.")






def GetLocationDeprecated(ip_address):
    """
    This function make the reader object everytime we call it 
    that is not enhanced at all
    """    
    
    location_data = {'ip': ip_address}
    try:
        # Create a reader object. It's better to initialize this once and reuse it.
        reader = database.Reader(GEOIP_DATABASE_PATH)

        response = reader.city(ip_address)

        location_data.update({
            'country_code': response.country.iso_code,
            'country_name': response.country.name,
            'state': response.subdivisions.most_specific.name,
            'city': response.city.name,
            'postal_code': response.postal.code,
            'latitude': response.location.latitude,
            'longitude': response.location.longitude,
            'timezone': response.location.time_zone,
        })
        reader.close()
    except errors.AddressNotFoundError:
        location_data['error'] = f"Location for IP address {ip_address} not found in the database."
    except Exception as e:
        location_data['error'] = str(e)
    return location_data

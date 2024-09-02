import socket
import math
import geoip2.errors
from django.contrib.gis.geoip2 import GeoIP2
from product.models import Location

R = 6378.1


def get_visitor_ip(meta: dict):
    try:
        return meta['HTTP_X_FORWARDED_FOR'].split(',')[0]
    except (KeyError, IndexError):
        return meta['REMOTE_ADDR']


def ip_is_valid(ip):
    try:
        socket.inet_aton(ip)
        GeoIP2().coords(ip)
        return True
    except (socket.error, geoip2.errors.AddressNotFoundError):
        return False


def _get_distance(lat1, lon1, lat2, lon2):
    lon1 = math.radians(float(lon1))
    lon2 = math.radians(float(lon2))
    lat1 = math.radians(float(lat1))
    lat2 = math.radians(float(lat2))

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def choose_closest(ip_info, stores_query):
    results = []
    lat1 = ip_info['latitude']
    lon1 = ip_info['longitude']
    for store in stores_query:
        lat2 = store.store_lat
        lon2 = store.store_long
        results.append((store.store_id, _get_distance(lat1, lon1, lat2, lon2)))
    return min(results, key=lambda x: x[1])[0]


def get_closest(request):
    g = GeoIP2()
    ip = get_visitor_ip(request.META)
    if ip_is_valid(ip):
        location_info = g.city(ip)
        stores = Location.objects.filter(state=location_info['region'])
        if not len(stores):
            closest = choose_closest(location_info, Location.objects.all())
        elif len(stores) == 1:
            closest = stores[0].store_id
        else:
            closest = choose_closest(location_info, stores)
    else:
        closest = Location.objects.first().store_id
    return closest

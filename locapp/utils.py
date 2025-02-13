from django.contrib.gis.geoip2 import GeoIP2


#creating my project helper functions here
def get_ip_address(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        
    return ip

def get_geo(ip):

    g = GeoIP2()
    city = g.city(ip)
    country = g.country(ip)
    lat, lon = g.lat_lon(ip)

    return city, country, lat, lon

def get_center_coordinates(latA, longA, latB=None, longB=None):
    cord = (latA, longA)
    if latB:
        cord = [(latA+latB)/2, (longA+longB)/2]
    return cord

def get_zoom(distance):

    if distance <= 100:
        return 15
    elif distance > 100 and distance <= 2500:
        return 5
    elif distance > 2501 and distance <= 3000:
        return 3
    else:
        return 2


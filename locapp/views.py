from django.shortcuts import render, get_object_or_404
from .models import Destination
from locapp.forms import DestinationForm
from geopy.geocoders import Nominatim
from .utils import get_ip_address, get_geo, get_center_coordinates, get_zoom
from geopy.distance import geodesic
import folium

# Create your views here.
def DestinationView(request):
    # obj = get_object_or_404(Destination, id=1)

    geolocator = Nominatim(user_agent='locapp')
    
    # ip = get_ip_address(request)
    # print(ip)

    ip = '115.186.189.2'
    city, country, lat, lon = get_geo(ip)
    #the function is passed with the ip address of the tourist to retrieve his/her location
    #the returned values are in the form of dictionaries
    # print('User City', city)
    # print('User Country', country)
    # print('Location Long', lon)
    # print('Location Lat', lat)

    #to get info about tourist in simple terms and not in the form of dictionary
    #here below I'll extract specific details of city using Nominatim instance
    touristcity = geolocator.geocode(city)
    # print(touristcity)

    tourist_lat = lat
    tourist_lon = lon
    touristLocation = (tourist_lat, tourist_lon)

    #Map using folium library
    #the map will point to the location of tourist
    mapobj = folium.Map(width=550, height=450, location=touristLocation, zoom_start=7)
    folium.Marker([tourist_lat, tourist_lon], tooltip= 'Click to get the name of city', popup=city['city'],
                        icon=folium.Icon(color='green')).add_to(mapobj)

    if request.method == "POST":
        fm = DestinationForm(request.POST)
        if fm.is_valid():
            fmwait = fm.save(commit=False)
            destination_ = fm.cleaned_data['destination']
            destination = geolocator.geocode(destination_)
            # print(destination.address)
            # print(destination.latitude)
            dest_lat = destination.latitude
            # print(destination.longitude)
            dest_long = destination.longitude
            
            destinationLocation = (dest_lat, dest_long)

            #Now calculating the distance between tourist location and distance location
            distance = geodesic(touristLocation, destinationLocation).km

            #Now to plot the route between tourist location and the destination
            mapobj = folium.Map(width=700, height=450, location=get_center_coordinates(tourist_lat, tourist_lon,dest_lat,dest_long),
                                 zoom_start=get_zoom(distance))
            #TouristLocation
            folium.Marker([tourist_lat, tourist_lon], tooltip= 'Click to get the name of city', popup=city['city'],
                        icon=folium.Icon(color='green')).add_to(mapobj)
            #TouristDestination
            folium.Marker([dest_lat, dest_long], tooltip= 'Click to get the name of city', popup=destination,
                        icon=folium.Icon(color='red', icon='cloud')).add_to(mapobj)
            #Now we will draw line between touristlocation and tourist destination
            line = folium.PolyLine(locations=[touristLocation, destinationLocation], weight=2, color='blue')
            #adding the line to our map now
            mapobj.add_child(line)

            fmwait.location = touristcity
            fmwait.distance = distance
            fmwait.save()


    #rendering foliummap in template    
    mapobj = mapobj._repr_html_()
    

    fm = DestinationForm()
    return render(request,'locapp/index.html', context={'form':fm, 'map': mapobj,})



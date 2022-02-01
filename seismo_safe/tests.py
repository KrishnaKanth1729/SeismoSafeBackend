from django.test import TestCase


from model.seismo_safe_model import SeismoSafeModel


k = SeismoSafeModel(lat=23.5335, lon=70.3242, area=150)
# print(k.json())






from geopy import Nominatim

def geolocation(place: str):
    nom = Nominatim(user_agent="myGeocoder")
    location = nom.geocode(place)
    return location.latitude, location.longitude

print(geolocation("Chobari"))
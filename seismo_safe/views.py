from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request

from .model.seismo_safe_model import SeismoSafeModel

import geopy

from typing import Tuple


def geolocation(place: str) -> Tuple[float, float]:
    """
    Function to geocode the name of a place to its latitude and longitude
    uses geopy.Nominatim
    """
    nom = geopy.Nominatim(user_agent="myGeocoder")
    location = nom.geocode(place)

    return (location.latitude, location.longitude)


@api_view(['POST'])
def index(request: Request) -> Response:
    """
    API endpoint for SeismoSafe

    Allowed Methods
        - POST
    
    Data is to be form of JSON
    ```json
        {
            "location": "Bangalore"
        }
    ```
    """

    if request.method == 'POST':
        try:
            lat, lon = geolocation(request.data['location'])
        except geopy.exc.GeocoderUnavailable:
            return Response({"message": "too many requests"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        model = SeismoSafeModel(lat, lon, 150)
        return Response(model.json(), status=status.HTTP_200_OK)
    else:
        print(f"Method {request.method} not allowed")

    return Response({})


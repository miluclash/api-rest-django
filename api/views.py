from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import GooglePlacesServices
from .serializers import PlaceSerializer
# Create your views here.
class NearbyTestView(APIView):
    """
    Vista de prueba para validar la conexión con Google Places API Nearby Search.
    URL sugerida: /api/test-nearby/?lat=40.4167&long=-3.7037
    """
    def get(self, request):
        # 1. Extraer parámetros de la URL
        lat = request.query_params.get('lat')
        long = request.query_params.get('long')

        # 2. Validación básica
        if not lat or not long:
            return Response(
                {"error": "Faltan los parámetros 'lat' y 'lng' en la URL"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 3. Llamamos al servicio que creamos antes
            # Convertimos a float para asegurar precisión matemática
            raw_data = GooglePlacesServices.search_places_nearBy(
                lat=float(lat), 
                long=float(long), 
                # radius=1500.0
            )

            if raw_data and 'places' in raw_data:
                # PASO CLAVE: Serializamos la lista de lugares
                serializer = PlaceSerializer(raw_data['places'], many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response({"results": []}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
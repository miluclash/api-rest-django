import datetime
import json
from external_servicies.wikidata import wikidata_crime
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from external_servicies.google_places import GooglePlacesServices
from .serializers import PlaceSerializer
from rest_framework.decorators import api_view



def api_view_andrea(request):
    # Mchael - frontend
    # 1 Wikidata

    # Jonathana
    # 1 PlacesNew

    # Handrea
    # 1 Clima
    # 2 Pokemon

    return HttpResponse(json.dumps({
        "message": "Hello, World!"
    }), content_type="application/json")

def api_view_michael(request):
    # Mchael    
    # 1 Wikidata

    # Jonathan
    # 1 PlacesNew

    # Handrea
    # 1 Clima
    # 2 Pokemon

    return HttpResponse(json.dumps({
        "message": "Hello, World!"
    }), content_type="application/json")


@api_view(['GET'])
def api_view_jonathan(request):
    # Mchael    
    # 1 Wikidata

    # Jonathana
    # 1 PlacesNew

    # Handrea
    # 1 Clima
    # 2 Pokemon

    date = request.query_params.get('date', datetime.datetime.now().strftime("%Y-%m-%d"))

    try:
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
    except (ValueError, TypeError):
        return HttpResponse(json.dumps({
            "code": 400,
            "msg": "Invalid date format. Please use YYYY-MM-DD."
        }), content_type="application/json", status=400)


    searching_crime= wikidata_crime('ApiFp/0.1 (aticasmia007@gmail.com)')

    crime = searching_crime.get_crime(date)

    return HttpResponse(json.dumps({
        "code": 200,
        "msg": f'{{weather.city}}, {{weather.temp}}°C, {{weather.desc}}. Un {{pokemon.name}} tipo {{pokemon.types}} con las manos sucias y "{crime['itemLabel']}" en el expediente. Nadie pregunta, nadie responde. {{restaurant.name}} sirve cocina {{restaurant.cuisine}} hasta las 11pm. Suficiente tiempo para olvidar todo.'
    }), content_type="application/json")

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

class SearchTextView(APIView):
    def get(self, request):
        #Parametros del endpoint
        lat = request.query_params.get('lat')
        long = request.query_params.get('long')
        query = request.query_params.get('textQuery')

        #Validacion basica
        if not lat or not long :
            return Response(
                {"error": "Faltan los parametros 'lat' y 'long' en la URL."}
            )
        elif not query:
            return Response(
                {"error": "Faltan el texto de búsqueda."}
            )
        
        #Llamamos al servicio
        try:
            raw_data = GooglePlacesServices.search_places_by_text(
                query=query
            )
            
            if raw_data and 'places' in raw_data:
                serializer = PlaceSerializer(raw_data['places'], many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response({"results": []}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


import datetime
import json
from external_servicies.wikidata import wikidata_crime
import secrets

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from external_servicies.google_places import GooglePlacesServices
from .serializers import PlaceSerializer
from rest_framework.decorators import api_view
from external_servicies.openweathermap import OpenWeatherMap
from external_servicies.pokeapi import PokeAPI
from dotenv import load_dotenv
import os

from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import UserAPIKey
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework import status
# Create your views here.

@api_view(['GET'])
def api_view_andrea(request):
    # Mchael - frontend
    # 1 Wikidata

    # Jonathana
    # 1 PlacesNew

    # Handrea
    # 1 Clima
    #Crear los parametros, que se pasan por url. <lat><lon>
    load_dotenv()
    api_key = os.getenv("OPENWEATHER_API_KEY")
    #Creo el objeto clima
    clima= OpenWeatherMap(api_key)
    #Creo diccionario de coordenadas recibidas por param
    lat= request.query_params.get("lat")
    lon = request.query_params.get("lon")

    coord = {
        "lat": lat, #seria lat lon
        "lon": lon
    }
    #Llamo al mé
    data_clima = clima.get_coord_forecast(coord)
    print(data_clima)
    #SACAR
    # 2 Pokemon
    #Utilizo los datos de data_clima!
    pokemon_creacion=PokeAPI()
    pokemon_elegido=pokemon_creacion.seleccionar_pokemon(data_clima["list"][0]["main"]["temp"], data_clima["list"][0]["wind"]["speed"], data_clima["list"][0]["weather"][0]["id"], data_clima["city"]['sun_visible'])
    #seguir desde aquí.

    return HttpResponse(json.dumps({
        "message": "api andrea funciona",
        "pokemonName": pokemon_elegido["name"],
        "types": pokemon_elegido["types"]
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
    # Para este endpoint se espera recibir los siguientes parámetros en la URL:
    # - date: Fecha en formato YYYY-MM-DD (opcional, por defecto se usará la fecha actual)
    # - lat: Latitud
    # - long: Longitud  
    date = request.query_params.get('date', datetime.datetime.now().strftime("%Y-%m-%d"))
    lat = request.query_params.get('lat')
    long = request.query_params.get('long')


    if not lat or not long:
        return HttpResponse(
            json.dumps({"error": "Faltan los parámetros 'lat' y 'lng' en la URL"}),
            content_type="application/json",
            status=status.HTTP_400_BAD_REQUEST
        )
    
    
    try:
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
    except (ValueError, TypeError):
        return HttpResponse(json.dumps({
            "code": 400,
            "msg": "Invalid date format. Please use YYYY-MM-DD."
        }), content_type="application/json", status=status.HTTP_400_BAD_REQUEST)

    try:
        searching_crime= wikidata_crime('ApiFp/0.1 (aticasmia007@gmail.com)')
        crime = searching_crime.get_crime(date)
    except Exception as e:
        return HttpResponse(json.dumps({
            "code": status.HTTP_400_BAD_REQUEST,
            "msg": "Error al obtener datos de Wikidata.",
        }), 
        content_type="application/json",status=status.HTTP_400_BAD_REQUEST)

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
            # print(raw_data['places'])
            serializer = PlaceSerializer(raw_data['places'], many=True)
            print(serializer.data)
    except Exception as e:
        return HttpResponse(
            json.dumps({"error": str(e)}),
            content_type="application/json",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

#    print(serializer.data)
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


# User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Ensure password is hashed
        password = self.request.data.get("password")
        user = serializer.save()

        if password:
            user.set_password(password)
            user.save()
            UserAPIKey.objects.create(user=user)


# User Profile (requires authentication)
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class RegenerateAPIKeyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        api_key = request.user.api_key
        api_key.key = secrets.token_hex(32)
        api_key.save()
        return Response({"api_key": api_key.key})

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
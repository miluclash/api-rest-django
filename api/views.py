import json

from django.http import HttpResponse
from django.shortcuts import render

from external_servicies.openweathermap import OpenWeatherMap
from external_servicies.pokeapi import PokeAPI
from dotenv import load_dotenv
import os
from rest_framework.decorators import api_view

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
    #Llamo al método para recibir el json
    data_clima = clima.get_coord_forecast(coord)

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

def api_view_jonathan(request):
    # Mchael    
    # 1 Wikidata

    # Jonathana
    # 1 PlacesNew

    # Handrea
    # 1 Clima
    # 2 Pokemon

    return HttpResponse(json.dumps({
        "message": "Hello, World!"
    }), content_type="application/json")
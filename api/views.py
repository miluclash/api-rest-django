import datetime
import json
from external_servicies.wikidata import wikidata_crime
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
# Create your views here.


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

    
    searching_crime= wikidata_crime('PruebaCrimenDjango/1.1 (aticasmia007@gmail.com)')
    today = datetime.datetime.now()
    crime = searching_crime.get_crime(today.strftime("%Y-%m-%d"))

    return HttpResponse(json.dumps({
        "code": 200,
        "msg": f'{{weather.city}}, {{weather.temp}}°C, {{weather.desc}}. Un {{pokemon.name}} tipo {{pokemon.types}} con las manos sucias y "{crime['itemLabel']}" en el expediente. Nadie pregunta, nadie responde. {{restaurant.name}} sirve cocina {{restaurant.cuisine}} hasta las 11pm. Suficiente tiempo para olvidar todo.'
    }), content_type="application/json")
import json

from django.http import HttpResponse
from django.shortcuts import render

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
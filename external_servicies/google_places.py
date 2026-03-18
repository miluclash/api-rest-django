"""Este archivo sirve como servicio para las vistas 
    Es como lo que realizaba en Postman , pero con python puro"""
    
import requests
from django.conf import settings

class GooglePlacesServices:
    
    @staticmethod
    def search_places_by_text(query, location_bias = None):
        """Metodo para busqueda por texto"""
        url = "https://places.googleapis.com/v1/places:searchText"
        
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key" : settings.GOOGLE_PLACES_API_KEY,#settings.GOOGLE_PLACES_API_KEY,PARA QUE EL TEST NO USE DJANGO LE PASAMOS DIRECTAMENTE LA API KEY
            "X-Goog-FieldMask" : "places.id,places.displayName,places.formattedAddress,places.currentOpeningHours.openNow,places.rating", 
        }
        #RAW de Postman
        payload = {
            "textQuery" : query,
            "languageCode" : "es",
            "maxResultCount" : 5,
        }
        
        if location_bias:
            payload['locationBias'] = location_bias

        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return {"error": "API key inválida o no autorizada"}
        elif response.status_code == 400:
            return {"error": "Petición incorrecta, revisa los parámetros"}
        else:
            return {"error": f"Error inesperado: {response.status_code}"}
    
    
    @staticmethod
    def search_places_nearBy(lat, long):
        """Metodo para busqueda cercana al usuario
        Este metodo recibe un par de coordenadas; Longitud y Latitud
        Segun el mecanismo SC2 de Google para buscar lugares, solo necesitariamos las coordenadas del 
        centro del radio de busqueda.
        Recibimos un diccionario con claves 'longitude' y 'latitude'"""
    
        url = "https://places.googleapis.com/v1/places:searchNearby" 
        
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key" : settings.GOOGLE_PLACES_API_KEY,
            "X-Goog-FieldMask" : "places.displayName,places.location,places.currentOpeningHours.openNow,places.formattedAddress,places.rating,places.priceRange", 
        }
        
        payload = {
            "includedTypes": ["restaurant"],
            "maxResultCount": 5,
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": lat,
                        "longitude": long
                    },
                    "radius": 3000.0 # Radio de 3 km
                    }
            }
        }
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return {"error": "API key inválida o no autorizada"}
        elif response.status_code == 400:
            return {"error": "Petición incorrecta, revisa los parámetros"}
        else:
            # TODO: Manejar otros códigos de error según la documentación de Google Places API
            return {"error": f"Error inesperado: {response.status_code}"}

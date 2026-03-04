"""Este archivo sirve como servicio para las vistas 
    Es como lo que realizaba en Postman , pero con python puro"""
    
import requests
from django.conf import settings

class GooglePlacesServices:
    """Metodo para busqueda por texto"""
    @staticmethod
    def search_places_by_text(query, location_bias = None):
        url = "https://places.googleapis.com/v1/places:searchText"
        
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key" : settings.GOOGLE_PLACES_API_KEY,
            "X-Goog-FieldMask" : "places.id,places.displayName,places.formattedAddress", 
        }
        #RAW de Postman
        payload = {
            "textQuery" : query,
            "languageCode" : "es",
            "maxResultCount" : 5,
        }
        
        if location_bias:
            payload['locationBias'] = location_bias

        #Django devuelve al frontend un JSON
        response = requests.post(url, json=payload, headers=headers)
        return response.json() if response.status_code == 200 else None
    
    
    """Metodo para busqueda cercana al usuario
        Este metodo recibe un par de coordenadas; Longitud y Latitud
        Segun el mecanismo SC2 de Google para buscar lugares, solo necesitariamos las coordenadas del 
        centro del radio de busqueda.
        Recibimos un diccionario con claves 'longitude' y 'latitude'"""
    @staticmethod
    def search_places_nearBy(lat, long):
        url = "https://places.googleapis.com/v1/places:searchNearby"
        
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key" : settings.GOOGLE_PLACES_API_KEY,
            "X-Goog-FieldMask" : "places.displayName,places.currentOpeningHours.openNow,places.formattedAddress,places.rating,places.priceRange", 
        }
        
        payload = {
            "includedTypes": ["restaurant"],
            "maxResultCount": 5,
            "locationRestriction": {
                "circle": {
                    "center": {
                        #Devuelve None si no tiene ubicacion especificada
                        "latitude": lat,
                        "longitude": long
                    },
                    "radius": 3000.0 # Radio de 3 km
                    }
            }
        }
        #Prueba para comprobar que Django obtiene correctamente la API-KEY
        print(f"DEBUG: Usando API KEY: {settings.GOOGLE_PLACES_API_KEY[:5]}...") # Solo muestra los primeros 5 caracteres por seguridad
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error en Google API: {response.status_code} - {response.text}")
            return None

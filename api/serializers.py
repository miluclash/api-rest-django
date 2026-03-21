from django.contrib.auth.models import User
from rest_framework import serializers

class PlaceSerializer(serializers.Serializer):
    # Definimos los campos que queremos mostrar al frontend
    #id = serializers.CharField()
    name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    rating = serializers.FloatField(required=False)
    location = serializers.SerializerMethodField()
    openNow = serializers.SerializerMethodField()

    # Métodos para "aplanar" la estructura de Google
    def get_name(self, obj):
        # Extrae el texto del objeto displayName
        return obj.get('displayName', {}).get('text', 'Sin nombre')

    def get_address(self, obj):
        # Google New usa formattedAddress
        return obj.get('formattedAddress', 'Dirección no disponible')

    def get_location(self, obj):
        # Simplifica las coordenadas
        location = obj.get('location', {})
        return {
            "lat": location.get('latitude'),
            "lng": location.get('longitude')
        }

    def get_rating(self,obj):
        rating = obj.get('rating','Rating no definido')
        return rating

    def get_openNow(self,obj):
        openNow = obj.get('currentOpeningHours', {})
        return openNow.get('openNow')

    #def get_priceRange(self,obj)PENDIENTE DE IMPLEMENTAR MOSTRAR EL RANGO DE PRECIOS DEL LUGAR:
class UserSerializer(serializers.ModelSerializer):
    api_key = serializers.CharField(source="api_key.key", read_only=True)
    class Meta:
        model = User
        # We only expose basic user fields
        fields = ['id', 'username', 'email', 'is_staff', "api_key"]

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = ['username', 'password']
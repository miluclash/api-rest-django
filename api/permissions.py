from rest_framework.permissions import BasePermission

from api.models import UserAPIKey

class hasAPIKey(BasePermission):
    message = "Para acceder a este recurso, debes usar un api_key válido asociado a tu cuenta."

    def has_permission(self, request, view):
        token = request.query_params.get('ApiKey', '')
        if not token:
            return False
        try:
            api_key = UserAPIKey.objects.get(key=token)
            request.user = api_key.user
            return True
        except UserAPIKey.DoesNotExist:
            return False
    
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    api_key = serializers.CharField(source="api_key.key", read_only=True)
    class Meta:
        model = User
        # We only expose basic user fields
        fields = ['id', 'username', 'email', 'is_staff', "api_key"]
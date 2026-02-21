from django.urls import path
from .views import NearbyTestView

urlpatterns = [
    # Aquí ir añadiendo los endpoints.
    path('test-nearby/',NearbyTestView.as_view(), name='test-nearby'),
]
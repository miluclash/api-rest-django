from django.urls import path
from .views import NearbyTestView, SearchTextView

urlpatterns = [
    # Aquí ir añadiendo los endpoints.
    path('test-nearby/',NearbyTestView.as_view(), name='test-nearby'),
    path('wherepoketoday/',SearchTextView.as_view(), name='results'),
]
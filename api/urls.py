from django.urls import path
from . import views

urlpatterns = [
    # Aquí ir añadiendo los endpoints.
    path('jonathan/', views.api_view_jonathan, name='api_view_jonathan'),
    
]
from django.urls import path
from . import views

urlpatterns = [
    # Aquí ir añadiendo los endpoints.
    path("andrea/", views.api_view_andrea, name="andrea-view")
    
]
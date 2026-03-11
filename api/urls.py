from django.urls import path
from . import views
from .views import RegisterView, ProfileView, LoginView, LogoutView, RegenerateAPIKeyView

urlpatterns = [
    # Aquí ir añadiendo los endpoints.
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    #Regenera la api-key:
    path('regen/', RegenerateAPIKeyView.as_view(), name='regen'),
]
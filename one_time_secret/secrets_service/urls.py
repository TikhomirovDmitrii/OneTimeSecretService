from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_secret, name='generate_secret'),
    path('<str:secret_key>/', views.get_secret, name='get_secret'),
]
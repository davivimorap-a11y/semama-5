from django.urls import path
from .views import (
    lista_pokemones, crear_pokemon, eliminar_pokemon, editar_pokemon, 
    detalle_pokemon, crear_entrenador, editar_entrenador, eliminar_entrenador, 
    detalle_entrenador, crear_gimnasio, detalle_gimnasio, editar_gimnasio, 
    eliminar_gimnasio, buscar_pokemon_api, adivina_pokemon
)

app_name = 'gestion_pokemon'

urlpatterns = [
    path('api-pokemon/', buscar_pokemon_api, name='buscar_pokemon_api'),
    path('adivina/', adivina_pokemon, name='adivina_pokemon'),
    
    path('', lista_pokemones, name='lista_pokemones'),
    path('crear/', crear_pokemon, name='crear_pokemon'),
    path('eliminar/<int:pokemon_id>/', eliminar_pokemon, name='eliminar_pokemon'),
    path('editar/<int:pokemon_id>/', editar_pokemon, name='editar_pokemon'),
    path('pokemon/<int:pokemon_id>/', detalle_pokemon, name='detalle_pokemon'),

    path('entrenador/crear/', crear_entrenador, name='crear_entrenador'),
    path('entrenador/editar/<str:pk>/', editar_entrenador, name='editar_entrenador'),
    path('entrenador/eliminar/<str:pk>/', eliminar_entrenador, name='eliminar_entrenador'),
    path('entrenador/<str:pk>/', detalle_entrenador, name='detalle_entrenador'),

    path('gimnasio/crear/', crear_gimnasio, name='crear_gimnasio'),
    path('gimnasio/<int:pk>/', detalle_gimnasio, name='detalle_gimnasio'),
    path('gimnasio/editar/<int:pk>/', editar_gimnasio, name='editar_gimnasio'),
    path('gimnasio/eliminar/<int:pk>/', eliminar_gimnasio, name='eliminar_gimnasio'),
]
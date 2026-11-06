from django.contrib import admin
from .models import Pokemon, Gimnasio, Entrenador

# Registramos los modelos para que aparezcan en el panel de admin
admin.site.register(Pokemon)
admin.site.register(Gimnasio)
admin.site.register(Entrenador)
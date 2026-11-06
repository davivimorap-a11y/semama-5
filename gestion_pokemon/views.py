from django.shortcuts import render, redirect, get_object_or_404
from .models import Pokemon, Entrenador, Gimnasio
from .forms import PokemonForm, EntrenadorForm, GimnasioForm 


def lista_pokemones(request):
    pokemones = Pokemon.objects.all().order_by('nombre')[:15]
    entrenadores = Entrenador.objects.all().order_by('nombre')[:10]
    gimnasios = Gimnasio.objects.all()

    context = {
        'pokemones': pokemones,
        'entrenadores': entrenadores,
        'gimnasios': gimnasios,
    }

    return render(request, 'gestion_pokemon/index.html', context)


def crear_pokemon(request):
    if request.method == 'POST':
        form = PokemonForm(request.POST, request.FILES) # request.FILES es crucial para la imagen
        if form.is_valid():
            form.save()
            return redirect('gestion_pokemon:lista_pokemones')
    else:
        form = PokemonForm()
    
    return render(request, 'gestion_pokemon/crear_pokemon.html', {'form': form})

def eliminar_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    if request.method == 'POST':
        pokemon.delete()
        return redirect('gestion_pokemon:lista_pokemones')
    return render(request, 'gestion_pokemon/eliminar_pokemon.html', {'pokemon': pokemon})

def editar_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    if request.method == 'POST':
        form = PokemonForm(request.POST, request.FILES, instance=pokemon)
        if form.is_valid():
            form.save()
            return redirect('gestion_pokemon:lista_pokemones')
    else:
        form = PokemonForm(instance=pokemon)
    
    return render(request, 'gestion_pokemon/editar_pokemon.html', {'form': form, 'pokemon': pokemon})

def detalle_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    return render(request, 'gestion_pokemon/detalle_pokemon.html', {'pokemon': pokemon})


def crear_entrenador(request):
    if request.method == 'POST':
        form = EntrenadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_pokemon:lista_pokemones')
    else:
        form = EntrenadorForm()
    return render(request, 'gestion_pokemon/crear_entrenador.html', {'form': form})

def editar_entrenador(request, pk):
    entrenador = get_object_or_404(Entrenador, pk=pk)
    if request.method == 'POST':
        form = EntrenadorForm(request.POST, instance=entrenador)
        if form.is_valid():
            form.save()
            return redirect('gestion_pokemon:lista_pokemones')
    else:
        form = EntrenadorForm(instance=entrenador)
    return render(request, 'gestion_pokemon/editar_entrenador.html', {'form': form, 'entrenador': entrenador})

def eliminar_entrenador(request, pk):
    entrenador = get_object_or_404(Entrenador, pk=pk)
    if request.method == 'POST':
        entrenador.delete()
        return redirect('gestion_pokemon:lista_pokemones')
    return render(request, 'gestion_pokemon/eliminar_entrenador.html', {'entrenador': entrenador})

def detalle_entrenador(request, pk):
    entrenador = get_object_or_404(Entrenador, pk=pk)
    return render(request, 'gestion_pokemon/detalle_entrenador.html', {'entrenador': entrenador})

def crear_gimnasio(request):
    if request.method == 'POST':
        form = GimnasioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_pokemon:lista_pokemones')
    else:
        form = GimnasioForm()
    return render(request, 'gestion_pokemon/crear_gimnasio.html', {'form': form})

def detalle_gimnasio(request, pk):
    gimnasio = get_object_or_404(Gimnasio, pk=pk)
    return render(request, 'gestion_pokemon/detalle_gimnasio.html', {'gimnasio': gimnasio})

def editar_gimnasio(request, pk):
    gimnasio = get_object_or_404(Gimnasio, pk=pk)
    if request.method == 'POST':
        form = GimnasioForm(request.POST, instance=gimnasio)
        if form.is_valid():
            form.save()
            return redirect('gestion_pokemon:lista_pokemones')
    else:
        form = GimnasioForm(instance=gimnasio)
    return render(request, 'gestion_pokemon/editar_gimnasio.html', {'form': form, 'gimnasio': gimnasio})

def eliminar_gimnasio(request, pk):
    gimnasio = get_object_or_404(Gimnasio, pk=pk)
    if request.method == 'POST':
        gimnasio.delete()
        return redirect('gestion_pokemon:lista_pokemones')
    return render(request, 'gestion_pokemon/eliminar_gimnasio.html', {'gimnasio': gimnasio})

# Consulta de Pokémon usando la API pública PokeAPI
def buscar_pokemon_api(request):
    import json
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError

    nombre = request.GET.get("nombre", "").strip().lower()
    resultado = None
    error = None

    if nombre:
        try:
            url = f"https://pokeapi.co/api/v2/pokemon/{nombre}"
            peticion = Request(url, headers={"User-Agent": "PokedexWorld-Django/1.0"})
            with urlopen(peticion, timeout=8) as respuesta:
                datos = json.loads(respuesta.read().decode("utf-8"))

            resultado = {
                "nombre": datos["name"].capitalize(),
                "numero": datos["id"],
                "imagen": datos["sprites"]["other"]["official-artwork"]["front_default"]
                          or datos["sprites"]["front_default"],
                "peso": datos["weight"] / 10,
                "altura": datos["height"] / 10,
                "tipos": [tipo["type"]["name"].capitalize() for tipo in datos["types"]],
                "habilidades": [habilidad["ability"]["name"].capitalize()
                                for habilidad in datos["abilities"]],
                "experiencia": datos["base_experience"],
            }
        except HTTPError as exc:
            if exc.code == 404:
                error = "No encontramos ese Pokémon. Revisa el nombre o número."
            else:
                error = "La API respondió con un error. Intenta de nuevo."
        except (URLError, TimeoutError, ValueError, KeyError):
            error = "No fue posible conectarse con PokeAPI. Revisa tu conexión."

    return render(request, "gestion_pokemon/buscar_api.html", {
        "nombre_buscado": nombre,
        "resultado": resultado,
        "error": error,
    })

import random

def adivina_pokemon(request):
    import json
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError

    resultado = None
    error = None
    adivinado = False
    mensaje = None
    opciones = []

    # Generamos 3 IDs distintos para el Pokémon correcto y los distractores (ej: de la 1 a la 151)
    ids_disponibles = list(range(1, 152))
    
    if request.method == 'POST':
        pokemon_id = request.POST.get('pokemon_id')
        nombre_correcto = request.POST.get('nombre_correcto', '').strip().lower()
        intento = request.POST.get('intento', '').strip().lower()

        if intento == nombre_correcto:
            adivinado = True
            mensaje = f"¡Correcto! Era {nombre_correcto.capitalize()} 🎉"
        else:
            mensaje = f"¡Fallaste! Era {nombre_correcto.capitalize()} 😢"
        
        # Consultamos el Pokémon correcto para mostrar su imagen real al responder
        try:
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
            peticion = Request(url, headers={"User-Agent": "PokedexWorld-Django/1.0"})
            with urlopen(peticion, timeout=8) as respuesta:
                datos = json.loads(respuesta.read().decode("utf-8"))
            
            resultado = {
                "id": datos["id"],
                "nombre": datos["name"].lower(),
                "imagen": datos["sprites"]["other"]["official-artwork"]["front_default"] or datos["sprites"]["front_default"],
            }
        except Exception:
            error = "Error al cargar el Pokémon."

    else:
        # Petición GET: Elegimos 3 Pokémon aleatorios diferentes
        seleccionados = random.sample(ids_disponibles, 3)
        pokemon_correcto_id = seleccionados[0]

        try:
            # 1. Obtenemos el Pokémon principal a adivinar
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_correcto_id}"
            peticion = Request(url, headers={"User-Agent": "PokedexWorld-Django/1.0"})
            with urlopen(peticion, timeout=8) as respuesta:
                datos = json.loads(respuesta.read().decode("utf-8"))
            
            resultado = {
                "id": datos["id"],
                "nombre": datos["name"].lower(),
                "imagen": datos["sprites"]["other"]["official-artwork"]["front_default"] or datos["sprites"]["front_default"],
            }
            opciones.append(datos["name"].lower())

            # 2. Obtenemos los nombres de los otros 2 Pokémon incorrectos para las opciones
            for incorrecto_id in seleccionados[1:]:
                url_inc = f"https://pokeapi.co/api/v2/pokemon/{incorrecto_id}"
                peticion_inc = Request(url_inc, headers={"User-Agent": "PokedexWorld-Django/1.0"})
                with urlopen(peticion_inc, timeout=8) as resp_inc:
                    datos_inc = json.loads(resp_inc.read().decode("utf-8"))
                opciones.append(datos_inc["name"].lower())

            # Mezclamos las 3 opciones aleatoriamente para que la respuesta correcta no esté siempre en el mismo botón
            random.shuffle(opciones)

        except (URLError, TimeoutError, ValueError, KeyError):
            error = "No fue posible conectarse con PokeAPI."

    return render(request, "gestion_pokemon/adivina_pokemon.html", {
        "resultado": resultado,
        "error": error,
        "adivinado": adivinado,
        "mensaje": mensaje,
        "opciones": opciones,
    })
# Carga de datos de demostración para el proyecto Pokedex
# Ejecutar desde la carpeta que contiene manage.py:
# python manage.py shell < cargar_datos_pokemon.py

from urllib.request import urlopen
from django.core.files.base import ContentFile
from gestion_pokemon.models import Pokemon, Entrenador, Gimnasio

# 15 Pokémon de la primera generación. Los pesos están expresados en kg.
pokemon_data = [
    ("Bulbasaur", "0.60", "Planta/Veneno", "Espesura; Clorofila", "N.º 001. Tiene una semilla en el lomo que crece absorbiendo luz solar."),
    ("Ivysaur", "13.00", "Planta/Veneno", "Espesura; Clorofila", "N.º 002. El bulbo de su espalda crece y se prepara para florecer."),
    ("Venusaur", "100.00", "Planta/Veneno", "Espesura; Clorofila", "N.º 003. Su gran flor absorbe energía solar y desprende un aroma relajante."),
    ("Charmander", "8.50", "Fuego", "Mar Llamas; Poder Solar", "N.º 004. La llama de su cola indica su estado físico y emocional."),
    ("Charmeleon", "19.00", "Fuego", "Mar Llamas; Poder Solar", "N.º 005. Tiene un carácter intenso y una llama muy caliente en la cola."),
    ("Charizard", "90.50", "Fuego/Volador", "Mar Llamas; Poder Solar", "N.º 006. Puede volar y lanzar llamaradas capaces de fundir rocas."),
    ("Squirtle", "9.00", "Agua", "Torrente; Cura Lluvia", "N.º 007. Se protege dentro de su caparazón y dispara agua a presión."),
    ("Wartortle", "22.50", "Agua", "Torrente; Cura Lluvia", "N.º 008. Nada con rapidez y usa su cola para mantener el equilibrio."),
    ("Blastoise", "85.50", "Agua", "Torrente; Cura Lluvia", "N.º 009. Sus cañones del caparazón lanzan chorros de agua muy potentes."),
    ("Caterpie", "2.90", "Bicho", "Polvo Escudo; Fuga", "N.º 010. Se alimenta de hojas y se desplaza usando las ventosas de sus patas."),
    ("Metapod", "9.90", "Bicho", "Mudar", "N.º 011. Su caparazón es duro y protege al Pokémon mientras evoluciona."),
    ("Butterfree", "32.00", "Bicho/Volador", "Ojo Compuesto; Cromolente", "N.º 012. Sus alas liberan un polvo que puede ser tóxico o causar sueño."),
    ("Weedle", "3.20", "Bicho/Veneno", "Polvo Escudo; Fuga", "N.º 013. Tiene un pequeño aguijón venenoso en la cabeza."),
    ("Kakuna", "10.00", "Bicho/Veneno", "Mudar", "N.º 014. Permanece casi inmóvil mientras su cuerpo se transforma."),
    ("Beedrill", "29.50", "Bicho/Veneno", "Enjambre; Francotirador", "N.º 015. Defiende su territorio con sus aguijones y suele actuar en enjambre."),
]

print("Creando Pokémon...")
pokemon_objects = {}
for nombre, peso, tipo, habilidades, descripcion in pokemon_data:
    obj, created = Pokemon.objects.update_or_create(
        nombre=nombre,
        defaults={
            "peso": peso,
            "habilidades": habilidades,
            "naturaleza_elemento": tipo,
            "descripcion": descripcion,
        },
    )

    # Descarga el artwork oficial de la Pokédex para guardar una imagen local.
    numero = len(pokemon_objects) + 1
    image_url = (
        "https://raw.githubusercontent.com/PokeAPI/sprites/master/"
        f"sprites/pokemon/other/official-artwork/{numero}.png"
    )
    try:
        if not obj.imagen:
            with urlopen(image_url, timeout=20) as response:
                image_bytes = response.read()
            obj.imagen.save(
                f"{nombre.lower()}_{numero:03d}.png",
                ContentFile(image_bytes),
                save=False,
            )
        obj.save()
    except Exception as error:
        # Si no hay conexión, se conserva el registro. La imagen se puede subir
        # después desde el administrador de Django.
        print(f"  Aviso: no se pudo descargar la imagen de {nombre}: {error}")
        obj.save()

    pokemon_objects[nombre] = obj
    print(f"  {'Creado' if created else 'Actualizado'}: {nombre}")

# 8 líderes de gimnasio oficiales de Kanto y sus medallas.
gym_data = [
    ("Brock", "Roca", "Medalla Roca"),
    ("Misty", "Agua", "Medalla Cascada"),
    ("Lt. Surge", "Eléctrico", "Medalla Trueno"),
    ("Erika", "Planta", "Medalla Arcoíris"),
    ("Koga", "Veneno", "Medalla Alma"),
    ("Sabrina", "Psíquico", "Medalla Pantano"),
    ("Blaine", "Fuego", "Medalla Volcán"),
    ("Giovanni", "Tierra", "Medalla Tierra"),
]

print("Creando gimnasios...")
gym_objects = []
for lider, tipo, medalla in gym_data:
    obj, created = Gimnasio.objects.get_or_create(
        lider_del_gym=lider,
        defaults={
            "naturaleza_elemento": tipo,
            "medallas": medalla,
        },
    )
    if not created:
        obj.naturaleza_elemento = tipo
        obj.medallas = medalla
        obj.save()
    gym_objects.append(obj)
    print(f"  {'Creado' if created else 'Actualizado'}: {lider}")

# 10 entrenadores conocidos del universo Pokémon.
# Los documentos son identificadores ficticios de demostración, no datos reales.
trainer_data = [
    ("900000001", "Ash", "Ketchum", ["Pikachu", "Charizard", "Butterfree"]),
    ("900000002", "Misty", "Sin apellido conocido", ["Squirtle", "Wartortle", "Blastoise"]),
    ("900000003", "Brock", "Sin apellido conocido", ["Bulbasaur", "Ivysaur", "Venusaur"]),
    ("900000004", "Gary", "Oak", ["Charmander", "Charmeleon", "Charizard"]),
    ("900000005", "Red", "Sin apellido conocido", ["Bulbasaur", "Squirtle", "Pikachu"]),
    ("900000006", "Blue", "Oak", ["Caterpie", "Metapod", "Beedrill"]),
    ("900000007", "Dawn", "Sin apellido conocido", ["Piplup", "Pikachu", "Butterfree"]),
    ("900000008", "Serena", "Sin apellido conocido", ["Charmander", "Butterfree", "Weedle"]),
    ("900000009", "Cynthia", "Campeona", ["Venusaur", "Blastoise", "Beedrill"]),
    ("900000010", "Leon", "Campeón", ["Charizard", "Pikachu", "Kakuna"]),
]

# Para que todos los vínculos existan en este conjunto de 15 Pokémon,
# se sustituyen nombres que no pertenecen al conjunto por Pokémon cargados.
replacements = {
    "Piplup": "Squirtle",
}
print("Creando entrenadores...")
for documento, nombre, apellido, equipo in trainer_data:
    entrenador, created = Entrenador.objects.update_or_create(
        id_documento=documento,
        defaults={"nombre": nombre, "apellido": apellido},
    )
    equipo_final = [replacements.get(nombre_pokemon, nombre_pokemon) for nombre_pokemon in equipo]
    entrenador.pokemones.set([pokemon_objects[n] for n in equipo_final])

    # Asigna medallas de ejemplo de forma distribuida.
    if documento in ("900000001", "900000005", "900000009"):
        entrenador.medallas.set(gym_objects[:4])
    elif documento in ("900000002", "900000003", "900000004"):
        entrenador.medallas.set(gym_objects[:2])
    else:
        entrenador.medallas.set(gym_objects[4:6])

    print(f"  {'Creado' if created else 'Actualizado'}: {nombre} {apellido}")

print("\n¡Carga terminada!")
print(f"Pokémon registrados: {Pokemon.objects.count()}")
print(f"Entrenadores registrados: {Entrenador.objects.count()}")
print(f"Gimnasios registrados: {Gimnasio.objects.count()}")
print("Revisa los registros en /admin/. Los documentos de entrenadores son ficticios.")

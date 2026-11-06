from django.db import models

class Gimnasio(models.Model):
    lider_del_gym = models.CharField(max_length=100, verbose_name="Líder del Gimnasio")
    naturaleza_elemento = models.CharField(max_length=50, verbose_name="Naturaleza/Elemento del Gym")
    medallas = models.CharField(max_length=100, verbose_name="Medallas")

    def __str__(self):
        return f"Gimnasio de {self.lider_del_gym}"


class Pokemon(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    peso = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Peso")
    imagen = models.ImageField(upload_to='pokemones/', verbose_name="Imagen")
    habilidades = models.TextField(verbose_name="Habilidades")
    naturaleza_elemento = models.CharField(max_length=50, verbose_name="Naturaleza Elemento")
    descripcion = models.TextField(verbose_name="Descripción")

    def __str__(self):
        return self.nombre


class Entrenador(models.Model):
    id_documento = models.CharField(max_length=20, primary_key=True, verbose_name="ID Documento")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    
    pokemones = models.ManyToManyField(Pokemon, related_name="entrenadores", verbose_name="Pokemones")
    medallas = models.ManyToManyField(Gimnasio, related_name="entrenadores_ganadores", blank=True, verbose_name="Medallas")

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
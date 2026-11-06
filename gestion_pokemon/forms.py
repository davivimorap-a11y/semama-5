from django import forms
from .models import Pokemon, Entrenador, Gimnasio

class PokemonForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        fields = ['nombre', 'peso', 'imagen', 'habilidades', 'naturaleza_elemento', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Pikachu'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 6.0'}),
            'habilidades': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ej. Electricidad estática'}),
            'naturaleza_elemento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Eléctrico'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Breve descripción...'}),
        }

class EntrenadorForm(forms.ModelForm):
    class Meta:
        model = Entrenador
        fields = ['id_documento', 'nombre', 'apellido', 'pokemones', 'medallas']
        widgets = {
            'pokemones': forms.CheckboxSelectMultiple(),
            'medallas': forms.CheckboxSelectMultiple(),
        }

class GimnasioForm(forms.ModelForm):
    class Meta:
        model = Gimnasio
        fields = ['lider_del_gym', 'naturaleza_elemento', 'medallas']
        widgets = {
            'lider_del_gym': forms.TextInput(attrs={'placeholder': 'Ej. Brock'}),
            'naturaleza_elemento': forms.TextInput(attrs={'placeholder': 'Ej. Roca'}),
            'medallas': forms.TextInput(attrs={'placeholder': 'Ej. Medalla Roca'}),
        }
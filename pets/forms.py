from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Animal, AnimalPerdido, Avistamento, Morador

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nome')
    last_name = forms.CharField(max_length=30, required=True, label='Sobrenome')
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'username': 'Usuário',
        }

class MoradorForm(forms.ModelForm):
    # Campos explícitos para maior controle
    tipo_residencia = forms.ChoiceField(
        choices=[
            ('apartamento', 'Apartamento'),
            ('casa', 'Casa'),
            ('cobertura', 'Cobertura'),
            ('loft', 'Loft'),
        ],
            label='Tipo de Residência'
    )
    
    numero_residencia = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 101, Casa 5, Cobertura 1'
        }),
        label='Número'
    )
    
    class Meta:
        model = Morador
        fields = ['condominio', 'tipo_residencia', 'numero_residencia', 'telefone', 'foto_perfil']
        labels = {
            'condominio': 'Condomínio',
            'telefone': 'Telefone',
            'foto_perfil': 'Foto do Perfil (opcional)',
        }
        widgets = {
            'condominio': forms.Select(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={
                'placeholder': '(11) 99999-9999', 
                'class': 'form-control'
            }),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control'}),
        }

# Resto dos forms permanecem iguais...
class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = [
            'nome', 'tipo', 'raca', 'cor', 'sexo', 'porte', 'idade_aproximada',
            'caracteristicas', 'foto', 'microchip', 'vacinado', 'castrado', 'observacoes'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome do animal', 'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'raca': forms.TextInput(attrs={'placeholder': 'Ex: Labrador, SRD', 'class': 'form-control'}),
            'cor': forms.TextInput(attrs={'placeholder': 'Ex: Marrom, Branco e preto', 'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'porte': forms.Select(attrs={'class': 'form-control'}),
            'idade_aproximada': forms.NumberInput(attrs={'class': 'form-control'}),
            'caracteristicas': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'microchip': forms.TextInput(attrs={'class': 'form-control'}),
            'vacinado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'castrado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'observacoes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

class AnimalPerdidoForm(forms.ModelForm):
    class Meta:
        model = AnimalPerdido
        fields = [
            'data_perda', 'local_perda', 'descricao', 'recompensa',
            'contato_emergencia', 'whatsapp'
        ]
        widgets = {
            'data_perda': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'local_perda': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'recompensa': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'contato_emergencia': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AvistamentoForm(forms.ModelForm):
    class Meta:
        model = Avistamento
        fields = ['local', 'data_avistamento', 'descricao', 'foto', 'contato']
        widgets = {
            'data_avistamento': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'local': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'contato': forms.TextInput(attrs={'class': 'form-control'}),
        }

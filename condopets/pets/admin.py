from django.contrib import admin
from .models import Condominio, Morador, Animal, AnimalPerdido, Avistamento, Notificacao

@admin.register(Condominio)
class CondominioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'endereco', 'telefone', 'criado_em']
    search_fields = ['nome', 'endereco']

@admin.register(Morador)
class MoradorAdmin(admin.ModelAdmin):
    list_display = ['user', 'condominio', 'apartamento', 'telefone', 'ativo']
    list_filter = ['condominio', 'ativo']
    search_fields = ['user__first_name', 'user__last_name', 'apartamento']

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'proprietario', 'ativo', 'criado_em']
    list_filter = ['tipo', 'sexo', 'porte', 'ativo']
    search_fields = ['nome', 'raca', 'proprietario__user__first_name']

@admin.register(AnimalPerdido)
class AnimalPerdidoAdmin(admin.ModelAdmin):
    list_display = ['animal', 'status', 'data_perda', 'visualizacoes']
    list_filter = ['status', 'data_perda']
    search_fields = ['animal__nome', 'local_perda']

@admin.register(Avistamento)
class AvistamentoAdmin(admin.ModelAdmin):
    list_display = ['animal_perdido', 'usuario', 'local', 'data_avistamento']
    list_filter = ['data_avistamento']
    search_fields = ['animal_perdido__animal__nome', 'local']

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'tipo', 'lida', 'criada_em']
    list_filter = ['tipo', 'lida', 'criada_em']
    search_fields = ['titulo', 'usuario__username']


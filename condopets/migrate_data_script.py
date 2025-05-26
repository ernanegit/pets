# Script para migrar dados existentes
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'condopets.settings')
django.setup()

from pets.models import Morador

print("Migrando dados existentes...")
moradores = Morador.objects.all()
contador = 0

for morador in moradores:
    if hasattr(morador, 'apartamento') and morador.apartamento:
        if not morador.numero_residencia:
            morador.numero_residencia = morador.apartamento
            morador.tipo_residencia = 'apartamento'
            morador.save()
            contador += 1
            print(f"Migrado: {morador.user.get_full_name()} - {morador.numero_residencia}")

print(f"Migração concluída! {contador} registros atualizados.")

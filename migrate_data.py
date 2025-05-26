# Script Python para migrar dados existentes (execute se necessário)
# python manage.py shell

from pets.models import Morador

# Migrar dados existentes de apartamento para numero_residencia
moradores = Morador.objects.all()
for morador in moradores:
    if hasattr(morador, 'apartamento') and morador.apartamento:
        if not hasattr(morador, 'numero_residencia') or not morador.numero_residencia:
            morador.numero_residencia = morador.apartamento
            morador.tipo_residencia = 'apartamento'
            morador.save()
            print(f"Migrado: {morador.user.get_full_name()} - {morador.numero_residencia}")

print("Migração de dados concluída!")

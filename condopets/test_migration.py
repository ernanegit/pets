import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'condopets.settings')
django.setup()

from pets.models import Morador

try:
    # Testar se os campos existem
    morador_test = Morador.objects.first()
    if morador_test:
        print(f"Tipo residência: {morador_test.tipo_residencia}")
        print(f"Número residência: {morador_test.numero_residencia}")
    else:
        print("Não há moradores cadastrados ainda")
    
    print("✅ CAMPOS EXISTEM! Migração bem-sucedida.")
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    print("Execute a OPÇÃO 2 - Reset completo")

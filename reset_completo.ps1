# OPÇÃO 2: RESET COMPLETO DO BANCO
# Execute apenas se a Opção 1 falhar

Write-Host "ATENÇÃO: Isso apagará TODOS os dados!"
$confirmacao = Read-Host "Digite 'RESET' para confirmar o reset completo"

if ($confirmacao -eq "RESET") {
    Write-Host "Resetando banco de dados..."
    
    # Remover banco atual
    Remove-Item "db.sqlite3" -Force -ErrorAction SilentlyContinue
    
    # Remover migrações
    Remove-Item "pets\migrations\00*.py" -Force -ErrorAction SilentlyContinue
    
    # Recriar __init__.py
    "" | Out-File -FilePath "pets\migrations\__init__.py" -Encoding UTF8
    
    # Criar nova migração
    python manage.py makemigrations pets
    python manage.py migrate
    
    Write-Host "Reset concluído! Crie um novo superusuário:"
    Write-Host "python manage.py createsuperuser"
} else {
    Write-Host "Reset cancelado."
}

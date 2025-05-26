# CondoPets 🐾

Sistema completo para gestão de animais em condomínios residenciais, desenvolvido em Django.

## 📋 Funcionalidades

- **Cadastro de Moradores**: Sistema completo de registro com dados de residência
- **Gestão de Animais**: Cadastro detalhado de pets com fotos e informações
- **Animais Perdidos**: Sistema de alerta e busca para animais perdidos
- **Avistamentos**: Moradores podem reportar avistamentos de animais perdidos
- **Notificações**: Sistema interno de notificações para a comunidade
- **Interface Responsiva**: Design moderno com Bootstrap 5

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 4.x
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Banco de Dados**: SQLite (desenvolvimento)
- **Upload de Imagens**: Pillow
- **Formulários**: django-crispy-forms

## 📦 Instalação

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Passos para instalação

1. **Clone o repositório**
```bash
git clone https://github.com/ernanegit/pets.git
cd pets
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instale as dependências**
```bash
pip install -r requirements.txt
```

5. **Execute as migrações**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

7. **Execute o servidor de desenvolvimento**
```bash
python manage.py runserver
```

O sistema estará disponível em `http://127.0.0.1:8000/`

## 🎯 Como Usar

### Para Administradores
1. Acesse o painel admin em `/admin/`
2. Cadastre os condomínios do sistema
3. Gerencie moradores e animais se necessário

### Para Moradores
1. **Registro**: Crie sua conta informando dados pessoais e de residência
2. **Cadastro de Pets**: Adicione seus animais com fotos e informações detalhadas
3. **Reportar Perdidos**: Se um animal se perder, crie um alerta para a comunidade
4. **Avistamentos**: Ajude outros moradores reportando avistamentos

## 📁 Estrutura do Projeto

```
pets/
├── condopets/              # Configurações do Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── pets/                   # App principal
│   ├── models.py          # Modelos de dados
│   ├── views.py           # Lógica das views
│   ├── forms.py           # Formulários
│   ├── urls.py            # URLs do app
│   └── admin.py           # Configuração do admin
├── templates/             # Templates HTML
│   ├── base.html
│   ├── pets/
│   └── registration/
├── static/               # Arquivos estáticos
│   ├── css/
│   └── js/
├── media/               # Uploads de usuários
├── requirements.txt     # Dependências
└── manage.py           # Script de gerenciamento
```

## 🔧 Configuração para Produção

### Variáveis de Ambiente
Crie um arquivo `.env` com:
```
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
```

### Banco de Dados
Para produção, recomenda-se PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'condopets_db',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Contato

- **Desenvolvedor**: Ernane
- **GitHub**: [@ernanegit](https://github.com/ernanegit)

## 🎉 Agradecimentos

- Comunidade Django pela excelente documentação
- Bootstrap pela interface responsiva
- FontAwesome pelos ícones

---

⭐ Se este projeto foi útil para você, considere dar uma estrela!
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from .models import Animal, AnimalPerdido, Avistamento, Notificacao, Morador
from .forms import CustomUserCreationForm, MoradorForm, AnimalForm, AnimalPerdidoForm, AvistamentoForm

def home(request):
    """Página inicial do CondoPets"""
    animais_perdidos = AnimalPerdido.objects.filter(status='perdido').order_by('-criado_em')[:6]
    total_animais = Animal.objects.filter(ativo=True).count()
    total_perdidos = AnimalPerdido.objects.filter(status='perdido').count()
    
    context = {
        'animais_perdidos': animais_perdidos,
        'total_animais': total_animais,
        'total_perdidos': total_perdidos,
    }
    return render(request, 'pets/home.html', context)

def register(request):
    """Cadastro de novos moradores"""
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        morador_form = MoradorForm(request.POST, request.FILES)
        
        if user_form.is_valid() and morador_form.is_valid():
            user = user_form.save()
            morador = morador_form.save(commit=False)
            morador.user = user
            morador.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('home')
    else:
        user_form = CustomUserCreationForm()
        morador_form = MoradorForm()
    
    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'morador_form': morador_form
    })

@login_required
def meus_animais(request):
    """Lista os animais do morador logado"""
    try:
        morador = Morador.objects.get(user=request.user)
        animais = Animal.objects.filter(proprietario=morador, ativo=True)
    except Morador.DoesNotExist:
        messages.error(request, 'Você precisa completar seu cadastro de morador primeiro.')
        return redirect('home')
    
    return render(request, 'pets/meus_animais.html', {'animais': animais})

@login_required
def cadastrar_animal(request):
    """Cadastro de novos animais"""
    try:
        morador = Morador.objects.get(user=request.user)
    except Morador.DoesNotExist:
        messages.error(request, 'Você precisa completar seu cadastro de morador primeiro.')
        return redirect('home')
    
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            animal = form.save(commit=False)
            animal.proprietario = morador
            animal.save()
            messages.success(request, f'{animal.nome} foi cadastrado com sucesso!')
            return redirect('meus_animais')
    else:
        form = AnimalForm()
    
    return render(request, 'pets/cadastrar_animal.html', {'form': form})

def animal_detail(request, pk):
    """Detalhes de um animal específico"""
    animal = get_object_or_404(Animal, pk=pk, ativo=True)
    return render(request, 'pets/animal_detail.html', {'animal': animal})

def animais_perdidos(request):
    """Lista de animais perdidos com filtros"""
    animais = AnimalPerdido.objects.filter(status='perdido').select_related('animal__proprietario')
    
    # Filtros
    tipo = request.GET.get('tipo')
    if tipo:
        animais = animais.filter(animal__tipo=tipo)
    
    search = request.GET.get('search')
    if search:
        animais = animais.filter(
            Q(animal__nome__icontains=search) |
            Q(animal__raca__icontains=search) |
            Q(local_perda__icontains=search)
        )
    
    paginator = Paginator(animais, 12)
    page = request.GET.get('page')
    animais = paginator.get_page(page)
    
    return render(request, 'pets/animais_perdidos.html', {'animais': animais})

@login_required
def reportar_perdido(request, animal_id):
    """Reportar um animal como perdido"""
    try:
        morador = Morador.objects.get(user=request.user)
        animal = get_object_or_404(Animal, pk=animal_id, proprietario=morador)
    except Morador.DoesNotExist:
        messages.error(request, 'Você precisa completar seu cadastro de morador primeiro.')
        return redirect('home')
    
    if request.method == 'POST':
        form = AnimalPerdidoForm(request.POST)
        if form.is_valid():
            perdido = form.save(commit=False)
            perdido.animal = animal
            perdido.save()
            
            # Criar notificações para outros moradores
            criar_notificacao_animal_perdido(perdido)
            
            messages.success(request, f'Alerta de {animal.nome} perdido foi criado!')
            return redirect('animal_perdido_detail', pk=perdido.pk)
    else:
        form = AnimalPerdidoForm()
    
    return render(request, 'pets/reportar_perdido.html', {'form': form, 'animal': animal})

def animal_perdido_detail(request, pk):
    """Detalhes de um animal perdido"""
    perdido = get_object_or_404(AnimalPerdido, pk=pk)
    perdido.visualizacoes += 1
    perdido.save()
    
    avistamentos = perdido.avistamentos.all().order_by('-criado_em')
    
    return render(request, 'pets/animal_perdido_detail.html', {
        'perdido': perdido,
        'avistamentos': avistamentos
    })

@login_required
def reportar_avistamento(request, perdido_id):
    """Reportar avistamento de um animal perdido"""
    perdido = get_object_or_404(AnimalPerdido, pk=perdido_id, status='perdido')
    
    if request.method == 'POST':
        form = AvistamentoForm(request.POST, request.FILES)
        if form.is_valid():
            avistamento = form.save(commit=False)
            avistamento.animal_perdido = perdido
            avistamento.usuario = request.user
            avistamento.save()
            
            # Notificar o proprietário
            criar_notificacao_avistamento(avistamento)
            
            messages.success(request, 'Avistamento reportado com sucesso!')
            return redirect('animal_perdido_detail', pk=perdido.pk)
    else:
        form = AvistamentoForm()
    
    return render(request, 'pets/reportar_avistamento.html', {
        'form': form,
        'perdido': perdido
    })

def criar_notificacao_animal_perdido(perdido):
    """Criar notificações para moradores do mesmo condomínio"""
    moradores = Morador.objects.filter(
        condominio=perdido.animal.proprietario.condominio,
        ativo=True
    ).exclude(user=perdido.animal.proprietario.user)
    
    for morador in moradores:
        Notificacao.objects.create(
            usuario=morador.user,
            tipo='animal_perdido',
            titulo=f'{perdido.animal.nome} está perdido',
            mensagem=f'O {perdido.animal.get_tipo_display().lower()} {perdido.animal.nome} do apartamento {perdido.animal.proprietario.apartamento} está perdido.',
            link=f'/perdidos/{perdido.pk}/'
        )

def criar_notificacao_avistamento(avistamento):
    """Notificar o proprietário sobre avistamento"""
    Notificacao.objects.create(
        usuario=avistamento.animal_perdido.animal.proprietario.user,
        tipo='avistamento',
        titulo=f'Avistamento de {avistamento.animal_perdido.animal.nome}',
        mensagem=f'Seu animal foi avistado em {avistamento.local}',
        link=f'/perdidos/{avistamento.animal_perdido.pk}/'
    )

def custom_logout(request):
    """Logout personalizado para evitar erro 405"""
    logout(request)
    messages.success(request, 'Você saiu do sistema com sucesso!')
    return redirect('home')

def logout_page(request):
    """Página de logout com template"""
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Logout realizado com sucesso!')
        return render(request, 'registration/logged_out.html')
    else:
        # Se for GET, mostrar página de confirmação
        return render(request, 'registration/logout_confirm.html')

from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect

def simple_logout(request):
    """Logout simples e direto"""
    auth_logout(request)
    messages.success(request, 'Você saiu do sistema!')
    return HttpResponseRedirect('/')

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

class Condominio(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    endereco = models.TextField(verbose_name="Endereço")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(verbose_name="Email")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Condomínio'
        verbose_name_plural = 'Condomínios'

class Morador(models.Model):
    TIPOS_RESIDENCIA = [
        ('apartamento', 'Apartamento'),
        ('casa', 'Casa'),
        ('cobertura', 'Cobertura'),
        ('loft', 'Loft'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE, verbose_name="Condomínio")
    tipo_residencia = models.CharField(
        max_length=20, 
        choices=TIPOS_RESIDENCIA, 
        default='apartamento',
        verbose_name="Tipo de Residência"
    )
    numero_residencia = models.CharField(
        max_length=10, 
        verbose_name="Número",
        help_text="Número do apartamento/casa"
    )
    # Manter campo antigo para compatibilidade temporária
    apartamento = models.CharField(max_length=10, blank=True, null=True, verbose_name="Apartamento (Antigo)")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    foto_perfil = models.ImageField(upload_to='perfis/', blank=True, null=True, verbose_name="Foto do Perfil")
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.numero_residencia:
            tipo_display = self.get_tipo_residencia_display()
            return f"{self.user.get_full_name()} - {tipo_display} {self.numero_residencia}"
        elif self.apartamento:
            return f"{self.user.get_full_name()} - Apto {self.apartamento}"
        else:
            return f"{self.user.get_full_name()}"

    def save(self, *args, **kwargs):
        # Migrar dados do campo antigo para o novo
        if self.apartamento and not self.numero_residencia:
            self.numero_residencia = self.apartamento
            self.tipo_residencia = 'apartamento'
        super().save(*args, **kwargs)
        if self.foto_perfil:
            try:
                img = Image.open(self.foto_perfil.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.foto_perfil.path)
            except:
                pass

class Animal(models.Model):
    TIPOS_ANIMAL = [
        ('cao', 'Cão'),
        ('gato', 'Gato'),
        ('passaro', 'Pássaro'),
        ('outro', 'Outro'),
    ]
    
    SEXOS = [
        ('M', 'Macho'),
        ('F', 'Fêmea'),
    ]
    
    PORTES = [
        ('P', 'Pequeno'),
        ('M', 'Médio'),
        ('G', 'Grande'),
    ]

    proprietario = models.ForeignKey(Morador, on_delete=models.CASCADE, related_name='animais')
    nome = models.CharField(max_length=100, verbose_name="Nome")
    tipo = models.CharField(max_length=20, choices=TIPOS_ANIMAL, verbose_name="Tipo")
    raca = models.CharField(max_length=100, blank=True, verbose_name="Raça")
    cor = models.CharField(max_length=50, verbose_name="Cor")
    sexo = models.CharField(max_length=1, choices=SEXOS, verbose_name="Sexo")
    porte = models.CharField(max_length=1, choices=PORTES, verbose_name="Porte")
    idade_aproximada = models.PositiveIntegerField(help_text="Idade em anos", verbose_name="Idade")
    caracteristicas = models.TextField(blank=True, help_text="Características especiais, personalidade, etc.", verbose_name="Características")
    foto = models.ImageField(upload_to='animais/', blank=True, null=True, verbose_name="Foto")
    microchip = models.CharField(max_length=50, blank=True, verbose_name="Microchip")
    vacinado = models.BooleanField(default=False, verbose_name="Vacinado")
    castrado = models.BooleanField(default=False, verbose_name="Castrado")
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()}) - {self.proprietario.user.get_full_name()}"

    def get_absolute_url(self):
        return reverse('animal_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.foto:
            try:
                img = Image.open(self.foto.path)
                if img.height > 400 or img.width > 400:
                    output_size = (400, 400)
                    img.thumbnail(output_size)
                    img.save(self.foto.path)
            except:
                pass

    class Meta:
        verbose_name = 'Animal'
        verbose_name_plural = 'Animais'
        ordering = ['-criado_em']

class AnimalPerdido(models.Model):
    STATUS_CHOICES = [
        ('perdido', 'Perdido'),
        ('encontrado', 'Encontrado'),
        ('cancelado', 'Cancelado'),
    ]

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='perdidos')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='perdido', verbose_name="Status")
    data_perda = models.DateTimeField(verbose_name="Data da Perda")
    local_perda = models.CharField(max_length=200, help_text="Local onde foi visto pela última vez", verbose_name="Local da Perda")
    descricao = models.TextField(help_text="Circunstâncias da perda, comportamento do animal, etc.", verbose_name="Descrição")
    recompensa = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Recompensa")
    contato_emergencia = models.CharField(max_length=100, blank=True, verbose_name="Contato de Emergência")
    whatsapp = models.CharField(max_length=20, blank=True, verbose_name="WhatsApp")
    visualizacoes = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.animal.nome} - {self.get_status_display()}"

    def get_absolute_url(self):
        return reverse('animal_perdido_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Animal Perdido'
        verbose_name_plural = 'Animais Perdidos'
        ordering = ['-criado_em']

class Avistamento(models.Model):
    animal_perdido = models.ForeignKey(AnimalPerdido, on_delete=models.CASCADE, related_name='avistamentos')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    local = models.CharField(max_length=200, verbose_name="Local")
    data_avistamento = models.DateTimeField(verbose_name="Data do Avistamento")
    descricao = models.TextField(verbose_name="Descrição")
    foto = models.ImageField(upload_to='avistamentos/', blank=True, null=True, verbose_name="Foto")
    contato = models.CharField(max_length=100, blank=True, verbose_name="Contato")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avistamento de {self.animal_perdido.animal.nome} - {self.local}"

    class Meta:
        verbose_name = 'Avistamento'
        verbose_name_plural = 'Avistamentos'
        ordering = ['-criado_em']

class Notificacao(models.Model):
    TIPOS = [
        ('animal_perdido', 'Animal Perdido'),
        ('avistamento', 'Avistamento'),
        ('encontrado', 'Animal Encontrado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS, verbose_name="Tipo")
    titulo = models.CharField(max_length=200, verbose_name="Título")
    mensagem = models.TextField(verbose_name="Mensagem")
    lida = models.BooleanField(default=False, verbose_name="Lida")
    link = models.URLField(blank=True, verbose_name="Link")
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-criada_em']

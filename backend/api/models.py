from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid

# --- GERENCIADOR DE USUÁRIO SIMPLIFICADO ---

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Cria e salva um usuário com o email e senha fornecidos.
        """
        if not email:
            raise ValueError("O email deve ser definido")
        email = self.normalize_email(email)
        
        model_extra_fields = extra_fields.copy() 
        if 'password' in model_extra_fields:
            del model_extra_fields['password']

        user = self.model(email=email, **model_extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("tipo_usuario", "Administrador")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    TIPO_USUARIO_CHOICES = (
        ('Cliente', 'Cliente'),
        ('Vendedor', 'Vendedor'),
        ('Administrador', 'Administrador'),
    )
    
    email = models.EmailField(unique=True)
    tipo_usuario = models.CharField(max_length=15, choices=TIPO_USUARIO_CHOICES, default='Cliente')
    
    # Campos requeridos pelo Django Admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Campos para verificação de email e reset de senha
    email_verificado = models.BooleanField(default=False)
    token_verificacao = models.UUIDField(null=True, blank=True)
    token_verificacao_expiracao = models.DateTimeField(null=True, blank=True)
    token_redefinir_senha = models.UUIDField(null=True, blank=True)
    token_redefinir_senha_expiracao = models.DateTimeField(null=True, blank=True)

    # Define o manager customizado
    objects = UsuarioManager()

    # Define o campo de login
    USERNAME_FIELD = 'email'
    # Campos requeridos para o comando createsuperuser (além de email e senha)
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Estoque(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='estoque_items')
    item = models.CharField(max_length=255)
    variacao = models.CharField(max_length=255, blank=True, null=True)
    quantidade = models.IntegerField(default=0)
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('usuario', 'item', 'variacao') # A user can have only one unique item/variation combination

    def __str__(self):
        return f"{self.item} ({self.variacao}) - {self.quantidade} - R${self.preco}"

class Venda(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='vendas')
    estoque_item = models.ForeignKey(Estoque, on_delete=models.PROTECT, related_name='vendas_realizadas')
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    preco_total = models.DecimalField(max_digits=10, decimal_places=2)
    data_venda = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure preco_unitario is set from estoque_item if not provided
        if not self.preco_unitario and self.estoque_item:
            self.preco_unitario = self.estoque_item.preco
        # Calculate preco_total
        self.preco_total = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venda de {self.quantidade}x {self.estoque_item.item} por {self.usuario.email}"

class Atividade(models.Model):
    PERIODO_CHOICES = (
        ('manha', 'Manhã'),
        ('tarde', 'Tarde'),
        ('noite', 'Noite'),
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='atividades')
    nome_atividade = models.CharField(max_length=255)
    periodo = models.CharField(max_length=10, choices=PERIODO_CHOICES, default='manha')
    ativa = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'nome_atividade')

    def __str__(self):
        return self.nome_atividade

class DiarioBordo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='diario_bordo')
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE, related_name='entradas_diario')
    data = models.DateTimeField()
    data_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data']

    def __str__(self):
        return f"{self.usuario.email} - {self.atividade.nome_atividade} em {self.data.strftime('%d/%m/%Y')}"

class RPD(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='rpd_entries')
    data = models.DateTimeField()
    situacao = models.TextField()
    pensamento_automatico = models.TextField()
    emocao = models.CharField(max_length=255)
    resposta_adaptativa = models.TextField()
    resultado = models.TextField()
    data_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data']
        verbose_name = "Registro de Pensamento Disfuncional"
        verbose_name_plural = "Registros de Pensamentos Disfuncionais"

    def __str__(self):
        return f"RPD de {self.usuario.email} em {self.data.strftime('%d/%m/%Y')}"

class LogPODDiario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='log_pod_diario_entries')
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE, related_name='log_pod_diario_entries')
    data = models.DateTimeField()
    status = models.BooleanField(default=False)
    data_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data']
        verbose_name = "Log POD Diário"
        verbose_name_plural = "Logs POD Diários"

    def __str__(self):
        return f"Log de {self.usuario.email} para {self.atividade.nome_atividade} em {self.data.strftime('%d/%m/%Y')}"
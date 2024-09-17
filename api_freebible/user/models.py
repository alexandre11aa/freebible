import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class BaseModelQuerySet(models.QuerySet):
    def delete(self):
        self.update(deleted_at=timezone.now(), is_active=False)

class BaseManager(models.Manager):
    def get_queryset(self):
        return BaseModelQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True, is_active=True)

class BaseModel(models.Model):
    created_at = models.DateTimeField('Created At', auto_now_add=True)
    updated_at = models.DateTimeField('Updated At', auto_now=True)
    deleted_at = models.DateTimeField('Deleted At', null=True, blank=True)
    is_active = models.BooleanField('Is Active', default=True)

    objects = BaseManager()

    def soft_delete(self, **kwargs):
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save()

    def hard_delete(self, **kwargs):
        super(BaseModel, self).delete(**kwargs)

    def recover(self):
        self.deleted_at = None
        self.is_active = True
        self.save()

    class Meta:
        abstract = True

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Cria e salva um usuário com o email e senha fornecidos.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Cria e salva um usuário com o email e senha fornecidos.
        """
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Cria e salva um superusuário com o email e senha fornecidos.
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True or extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_staff=True and is_superuser=True')

        return self._create_user(email, password, **extra_fields)

# Classe Pessoa
class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):

    is_staff = models.BooleanField(
        'Moderador',
        default=False,
        help_text='Designa se o usuário pode logar no site do admin.'
    )

    is_active = models.BooleanField(
        'Ativo',
        default=True,
        help_text='Designa se a conta está ativa.'
    )

    NE_CHOICES = [
        ('F', 'Deficiência física/motora'),
        ('I', 'Deficiência intelectual/mental'),
        ('V', 'Deficiência visual'),
        ('A', 'Deficiência auditiva'),
        ('M', 'Deficiência múltipla'),
    ]

    ESTADO_CIVIL_CHOICES = [
        ('S', 'Solteiro(a)'),
        ('C', 'Casado(a)'),
        ('D', 'Divorciado(a)'),
        ('V', 'Viúvo(a)'),
        ('U', 'União estável'),
    ]

    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
        ('N', 'Prefiro não informar'),
    ]

    RACA_CHOICES = [
        ('BR', 'Branca'),
        ('PR', 'Preta'),
        ('PA', 'Parda'),
        ('IN', 'Indígena'),
        ('AM', 'Amarela'),
    ]

    code = models.UUIDField("Código uuid4", default=uuid.uuid4, editable=False)
    matricula = models.IntegerField('Matrícula', unique=True)
    name = models.CharField('Name', max_length=255)
    nome_colaborador = models.CharField('Nome do Colaborador', max_length=255)
    necessidade_especial = models.CharField('Necessidade Especial', max_length=1, choices=NE_CHOICES, null=True, blank=True)
    estado_civil = models.CharField('Estado Civil', max_length=1, choices=ESTADO_CIVIL_CHOICES, null=True, blank=True)
    numero_tel = models.CharField('Número de Telefone', max_length=20, null=True, blank=True)
    nacionalidade = models.CharField('Nacionalidade', max_length=50, null=True, blank=True)
    sexo = models.CharField('Sexo', max_length=1, choices=SEXO_CHOICES, null=True, blank=True)
    raca = models.CharField('Raça', max_length=2, choices=RACA_CHOICES, null=True, blank=True)
    email = models.EmailField('Email', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'matricula']

    objects = UserManager()

    def __str__(self):
        return self.name
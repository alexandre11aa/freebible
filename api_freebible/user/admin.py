from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    
    # Campos exibidos na lista de usuários
    list_display = (
        'email', 'name', 'matricula', 'is_staff'
    )
    
    # Campos utilizados para pesquisa no painel administrativo
    search_fields = ('email', 'name', 'matricula', 'nome_colaborador')
    
    # Filtros disponíveis para filtrar usuários na lista
    list_filter = ('is_staff', 'sexo', 'raca', 'estado_civil', 'necessidade_especial')
    
    # Ordem de exibição dos usuários na lista
    ordering = ('matricula',)
    
    # Configurações para os formulários de edição e visualização
    fieldsets = (
        # Seção principal com campos básicos
        (None, {'fields': ('email', 'name', 'matricula', 'password')}),
        
        # Seção de informações pessoais com diversos campos adicionais
        ('Personal info', {
            'fields': ('is_staff', 'is_active', 'last_login', 'sexo', 'raca', 'estado_civil', 'necessidade_especial', 'numero_tel', 'nacionalidade', 'nome_colaborador')
        }),
        
        # Seção de permissões
        ('Permissions', {'fields': ('is_superuser',)}),
    )
    
    # Campos a serem exibidos ao adicionar um novo usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'matricula', 'password1', 'password2', 'is_staff', 'is_superuser', 'sexo', 'raca', 'estado_civil', 'necessidade_especial', 'numero_tel', 'nacionalidade', 'nome_colaborador')
        }),
    )
    
    filter_horizontal = ()
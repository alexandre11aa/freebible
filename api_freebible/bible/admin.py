from django.contrib import admin
from .models import *

@admin.register(Biblia)
class BibliaAdmin(admin.ModelAdmin):
    list_display = ('code', 'versao', 'lingua')
    search_fields = ('versao', 'lingua')
    list_filter = ('lingua',)

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('biblia', 'livro', 'testamento')
    search_fields = ('biblia__versao', 'livro')
    list_filter = ('testamento',)

@admin.register(Capitulo)
class CapituloAdmin(admin.ModelAdmin):
    list_display = ('livro', 'numero', 'autor')
    search_fields = ('livro__livro', 'autor')
    list_filter = ('livro',)

@admin.register(Versiculo)
class VersiculoAdmin(admin.ModelAdmin):
    list_display = ('capitulo', 'numero')
    search_fields = ('capitulo__livro__livro',)
    list_filter = ('capitulo',)
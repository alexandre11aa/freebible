"""
URL configuration for api_freebible project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Importando configurações do Django e as funções necessárias para definir as URLs
from django.conf import settings  # Importa o arquivo de configurações do Django
from django.conf.urls.static import static  # Usado para configurar as URLs de arquivos estáticos, como imagens, vídeos, etc.
from django.contrib import admin  # Importa o módulo de administração do Django
from django.urls import include, path, re_path  # Importa funções para configurar as rotas do Django, como `path`, `include` e `re_path`

# Importando as permissões do Django Rest Framework
from rest_framework import permissions  # Usado para configurar permissões em views da API

# Importando bibliotecas para gerar a documentação da API com Swagger
from drf_yasg import openapi  # Usado para criar a especificação OpenAPI que será usada pelo Swagger
from drf_yasg.views import get_schema_view  # Usado para gerar a visualização da documentação (UI) do Swagger

# Importando o roteador do app 'user' que registra as URLs da API
from user.urls import router_user  # Inclui as URLs do app 'user' para o roteador que define as rotas da API
from bible.urls import router_bible_version

# Configuração do Swagger
# O Swagger é uma ferramenta para gerar documentação interativa e bem formatada para APIs RESTful.
schema_view = get_schema_view(
    # Definindo as informações da API, como título, versão e descrição
    openapi.Info(
        title="Sua API",  # Título da API
        default_version='v1',  # Versão da API
        description="Descrição da sua API",  # Descrição da API
        terms_of_service="https://www.google.com/policies/terms/",  # Link para os termos de serviço
        contact=openapi.Contact(email="contato@exemplo.com"),  # Informações de contato (e-mail)
        license=openapi.License(name="Licença BSD"),  # Licença da API
    ),
    public=True,  # Define que a documentação estará disponível publicamente
    permission_classes=(permissions.AllowAny,),  # Permissões para permitir que qualquer usuário acesse a documentação
)

# Definindo as rotas (URLs) da aplicação
urlpatterns = [

    # Rota para a página de administração do Django
    path('admin/', admin.site.urls),
    
    # O roteador 'router_user' é registrado no app 'user' e define as rotas da API para o 'CustomUserViewSet'
    path('api/v1/user/', include(router_user.urls)),

    # O roteador 'router_bible_version' é registrado no app 'bible' e define as rotas da API para o 'BibliaViewSet'
    path('api/v1/bible/', include(router_bible_version.urls)),

    # Rota para gerar a documentação Swagger no formato JSON ou YAML
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # Rota para acessar a interface do Swagger (UI) que mostra a documentação interativa
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    # Rota para acessar a documentação da API usando o Redoc, que é uma outra interface de documentação
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
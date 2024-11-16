from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from bible.models import Biblia
from bible.serializers.bible import (BibliaSerializer,
                                     BibliaCreateSerializer,
                                     BibliaUpdateSerializer)

class BibliaViewSet(viewsets.ModelViewSet):

    ## Operacional Methods para urls

    # Define o queryset padrão que será utilizado para todas as ações (exceção para ações customizadas)
    queryset = Biblia.objects.all()
    serializer_class = BibliaSerializer

    def get_serializer_class(self):
        '''
        Método que seleciona o serializer correto dependendo da ação
        '''

        # Ação de criação usando código UUID
        if self.action == 'create':
            return BibliaCreateSerializer
        # Ações de atualização usando ID
        if self.action == 'update_by_id':
            return BibliaUpdateSerializer
        # Ação padrão para outros casos
        return BibliaSerializer

    def get_serializer_context(self):
        '''
        Contexto adicional do serializer (opcional)
        '''

        context = super().get_serializer_context()
        context['request'] = self.request  # Adiciona a requisição ao contexto
        return context

    ## Endpoints

    @action(detail=False, methods=['post'], url_path='create')
    def create_with_code(self, request):
        '''
        Ação personalizada para criar um Biblia
        '''

        # Instancia o serializer para criação de Biblia com código UUID
        serializer = BibliaCreateSerializer(data=request.data)

        if serializer.is_valid():
            bible_version = serializer.save()  # Cria o Biblia
            return Response({'code': bible_version.code}, status=status.HTTP_201_CREATED)  # Retorna o código UUID do usuário criado
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Retorna erros se inválido
        
        '''  # Shell
        curl -X POST http://127.0.0.1:8000/api/v1/bible/bible_version/create/ \
            -d "lingua=EN" \
            -d "versao=Almeida" \
            -u "admin@admin.com:admin"
        '''
 
    @action(detail=True, methods=['put', 'patch'], url_path='update_by_id')
    def update_by_id(self, request, pk=None):
        '''
        Ação personalizada para atualizar Biblia por ID
        '''

        # Busca o objeto Biblia pelo código ou ID
        if pk:
            instance = self.get_object()
        else:
            instance = None

        serializer_class = BibliaUpdateSerializer

        # Instancia o serializer para validação e salvamento
        serializer = serializer_class(
            instance, data=request.data, partial=request.method == 'PATCH', context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK if instance else status.HTTP_201_CREATED)
    
        '''  # Shell
        curl -X PUT http://127.0.0.1:8000/api/v1/bible/bible_version/2/update_by_id/ \
            -d "lingua=EN" \
            -d "versao=King" \
            -u "admin@admin.com:admin"
        '''

    @action(detail=False, methods=['delete'], url_path='delete_by_id/(?P<pk>[^/.]+)')
    def delete_by_id(self, request, pk=None):
        '''
        Ação personalizada para excluir Biblia por ID
        '''

        # Busca o Biblia por ID ou código
        instance = get_object_or_404(Biblia, pk=pk)
        instance.soft_delete()  # Exclui o objeto encontrado

        return Response(status=status.HTTP_204_NO_CONTENT)  # Retorna resposta de sucesso
    
        '''  # Shell
        curl -X DELETE http://127.0.0.1:8000/api/v1/bible/bible_version/delete_by_id/2/ \
            -u "admin@admin.com:admin"
        '''
    
    @action(detail=False, methods=['get'], url_path='get_by_id/(?P<pk>[^/.]+)')
    def get_by_id(self, request, pk=None):
        '''
        Ação personalizada para recuperar Biblia por ID
        '''

        # Busca o Biblia por ID ou código
        instance = get_object_or_404(Biblia, pk=pk)
        serializer = self.get_serializer(instance)

        return Response(serializer.data)  # Retorna os dados do usuário encontrado
    
        '''  # Shell
        curl -X GET http://127.0.0.1:8000/api/v1/bible/bible_version/get_by_id/1/ \
            -u "admin@admin.com:admin"
        '''
    
    @action(detail=False, methods=['get'], url_path='list_active')
    def list_active(self, request):
        '''
        Ação personalizada para listar usuários ativos
        '''

        queryset = Biblia.all_objects.filter(is_active=True)  # Filtra usuários pela condição de ativo/inativo
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)  # Retorna a lista de usuários filtrados
    
        '''  # Shell
        curl -X GET http://127.0.0.1:8000/api/v1/bible/bible_version/list_active/ \
            -u "admin@admin.com:admin"
        '''

    @action(detail=False, methods=['get'], url_path='list_inactive')
    def list_inactive(self, request):
        '''
        Ação personalizada para listar usuários inativos
        '''

        queryset = Biblia.all_objects.filter(is_active=False)  # Filtra usuários pela condição de ativo/inativo
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)  # Retorna a lista de usuários filtrados
    
        '''  # Shell
        curl -X GET http://127.0.0.1:8000/api/v1/bible/bible_version/list_inactive/ \
            -u "admin@admin.com:admin"
        '''

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        '''
        Ação personalizada para buscar registros da Bíblia com parâmetros específicos.
        '''

        query_params = request.query_params
        queryset = self.queryset

        # Aplica filtros baseados nos parâmetros da consulta
        for param, value in query_params.items():
            if param == 'lingua':
                # Filtro para campo `lingua` com correspondência exata
                queryset = queryset.filter(lingua=value)
            elif param == 'versao':
                # Filtro para campo `versao` com busca aproximada (case insensitive)
                queryset = queryset.filter(versao__icontains=value)
            elif param in [f.name for f in Biblia._meta.get_fields()]:
                # Filtros genéricos para outros campos do modelo
                queryset = queryset.filter(**{f"{param}__icontains": value})

        # Serializa a lista de resultados encontrados
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
        '''  # Shell
        curl -X GET "http://127.0.0.1:8000/api/v1/bible/bible_version/search/?lingua=PT" -u "admin@admin.com:admin"

        curl -X GET "http://127.0.0.1:8000/api/v1/bible/bible_version/search/?versao=Almeida" -u "admin@admin.com:admin"

        curl -X GET "http://127.0.0.1:8000/api/v1/bible/bible_version/search/?lingua=PT&versao=Almeida" -u "admin@admin.com:admin"        
        '''
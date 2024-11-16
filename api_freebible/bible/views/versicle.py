from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from bible.models import Versiculo
from bible.serializers.versicle import (VersiculoSerializer,
                                        VersiculoCreateSerializer,
                                        VersiculoUpdateSerializer)

class VersiculoViewSet(viewsets.ModelViewSet):

    ## Operacional Methods para urls

    # Define o queryset padrão que será utilizado para todas as ações (exceção para ações customizadas)
    queryset = Versiculo.objects.all()
    serializer_class = VersiculoSerializer

    def get_serializer_class(self):
        '''
        Método que seleciona o serializer correto dependendo da ação
        '''

        # Ação de criação usando código UUID
        if self.action == 'create':
            return VersiculoCreateSerializer
        # Ações de atualização usando ID
        if self.action == 'update_by_id':
            return VersiculoUpdateSerializer
        # Ação padrão para outros casos
        return VersiculoSerializer

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
        Ação personalizada para criar um Versiculo
        '''

        # Instancia o serializer para criação de Versiculo com código UUID
        serializer = VersiculoCreateSerializer(data=request.data)

        if serializer.is_valid():
            versicle = serializer.save()  # Cria o Versiculo
            return Response({'id': versicle.id}, status=status.HTTP_201_CREATED)  # Retorna o código UUID do usuário criado
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Retorna erros se inválido
        
        '''  # Shell
        curl -X POST http://127.0.0.1:8000/api/v1/bible/versicle/create/ \
            -d "capitulo=1" \
            -d "numero=4" \
            -d "versiculo=E disse Deus: Haja luz; e houve luz." \
            -u "admin@admin.com:admin"
        '''
 
    @action(detail=True, methods=['put', 'patch'], url_path='update_by_id')
    def update_by_id(self, request, pk=None):
        '''
        Ação personalizada para atualizar Versiculo por ID
        '''

        # Busca o objeto Versiculo pelo código ou ID
        if pk:
            instance = self.get_object()
        else:
            instance = None

        serializer_class = VersiculoUpdateSerializer

        # Instancia o serializer para validação e salvamento
        serializer = serializer_class(
            instance, data=request.data, partial=request.method == 'PATCH', context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK if instance else status.HTTP_201_CREATED)
    
        '''  # Shell
        curl -X PUT http://127.0.0.1:8000/api/v1/bible/versicle/3/update_by_id/ \
            -d "capitulo=1" \
            -d "numero=3" \
            -d "versiculo=E disse Deus: Haja luz; e houve luz." \
            -u "admin@admin.com:admin"
        '''

    @action(detail=False, methods=['delete'], url_path='delete_by_id/(?P<pk>[^/.]+)')
    def delete_by_id(self, request, pk=None):
        '''
        Ação personalizada para excluir Versiculo por ID
        '''

        # Busca o Versiculo por ID ou código
        instance = get_object_or_404(Versiculo, pk=pk)
        instance.soft_delete()  # Exclui o objeto encontrado

        return Response(status=status.HTTP_204_NO_CONTENT)  # Retorna resposta de sucesso
    
        '''  # Shell
        curl -X DELETE http://127.0.0.1:8000/api/v1/bible/versicle/delete_by_id/2/ \
            -u "admin@admin.com:admin"
        '''
    
    @action(detail=False, methods=['get'], url_path='get_by_id/(?P<pk>[^/.]+)')
    def get_by_id(self, request, pk=None):
        '''
        Ação personalizada para recuperar Versiculo por ID
        '''

        # Busca o Versiculo por ID ou código
        instance = get_object_or_404(Versiculo, pk=pk)
        serializer = self.get_serializer(instance)

        return Response(serializer.data)  # Retorna os dados do usuário encontrado
    
        '''  # Shell
        curl -X GET http://127.0.0.1:8000/api/v1/bible/versicle/get_by_id/1/ \
            -u "admin@admin.com:admin"
        '''
    
    @action(detail=False, methods=['get'], url_path='list_active')
    def list_active(self, request):
        '''
        Ação personalizada para listar usuários ativos
        '''

        queryset = Versiculo.all_objects.filter(is_active=True)  # Filtra usuários pela condição de ativo/inativo
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)  # Retorna a lista de usuários filtrados
    
        '''  # Shell
        curl -X GET http://127.0.0.1:8000/api/v1/bible/versicle/list_active/ \
            -u "admin@admin.com:admin"
        '''

    @action(detail=False, methods=['get'], url_path='list_inactive')
    def list_inactive(self, request):
        '''
        Ação personalizada para listar usuários inativos
        '''

        queryset = Versiculo.all_objects.filter(is_active=False)  # Filtra usuários pela condição de ativo/inativo
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)  # Retorna a lista de usuários filtrados
    
        '''  # Shell
        curl -X GET http://127.0.0.1:8000/api/v1/bible/versicle/list_inactive/ \
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
            if param == 'capitulo':
                # Filtro para o campo `capitulo` (relacionamento com o modelo Capitulo)
                queryset = queryset.filter(capitulo__id=value)
            elif param == 'numero':
                # Filtro para o campo `numero` (número do versículo)
                queryset = queryset.filter(numero=value)
            elif param == 'versiculo':
                # Filtro para o campo `versiculo` (conteúdo do versículo)
                queryset = queryset.filter(versiculo__icontains=value)  # Uso de `icontains` para correspondência parcial

        # Serializa a lista de resultados encontrados
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
        '''
        curl -X GET "http://127.0.0.1:8000/api/v1/bible/versicle/search/?capitulo=1" -u "admin@admin.com:admin"

        curl -X GET "http://127.0.0.1:8000/api/v1/bible/versicle/search/?numero=5" -u "admin@admin.com:admin"

        curl -X GET "http://127.0.0.1:8000/api/v1/bible/versicle/search/?versiculo=João" -u "admin@admin.com:admin"

        curl -X GET "http://127.0.0.1:8000/api/v1/bible/versicle/search/?capitulo=1&versiculo=E disse Deus: Haja luz; e houve luz." -u "admin@admin.com:admin"
        '''
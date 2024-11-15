from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CustomUser
from .serializers import (CustomUserSerializer,
                          CustomUserCreateWithCodeSerializer,
                          CustomUserCreateWithIDSerializer,
                          CustomUserUpdateByCodeSerializer,
                          CustomUserUpdateByIDSerializer)

class CustomUserViewSet(viewsets.ModelViewSet):

    ## Operacional Methods

    # Define o queryset padrão que será utilizado para todas as ações (exceção para ações customizadas)
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_serializer_class(self):
        '''
        Método que seleciona o serializer correto dependendo da ação
        '''

        # Ação de criação usando código UUID
        if self.action == 'create':
            return CustomUserCreateWithIDSerializer
        # Ação de criação usando código UUID para CustomUser
        if self.action == 'create_with_code':
            return CustomUserCreateWithCodeSerializer
        # Ações de atualização usando ID ou código UUID
        if self.action in ['update_by_id', 'update_by_code']:
            return CustomUserUpdateByIDSerializer if self.action == 'update_by_id' else CustomUserUpdateByCodeSerializer
        # Ação padrão para outros casos
        return CustomUserSerializer

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
        Ação personalizada para criar um CustomUser usando código UUID
        '''

        # Instancia o serializer para criação de CustomUser com código UUID
        custom_user_serializer = CustomUserCreateWithCodeSerializer(data=request.data)

        if custom_user_serializer.is_valid():
            custom_user = custom_user_serializer.save()  # Cria o CustomUser
            return Response({'code': custom_user.code}, status=status.HTTP_201_CREATED)  # Retorna o código UUID do usuário criado
        else:
            return Response(custom_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Retorna erros se inválido
        
        '''  # Shell
        curl -X POST http://127.0.0.1:8000/api/v1/consumer/custom_user/create/ \
            -d "email=test_create@test.com" \
            -d "nome=user_create" \
            -d "password=password123" \
            -u "admin@admin.com:admin"
        '''
 
    # @action(detail=False, methods=['put', 'patch'], url_path='update_by_code/(?P<code>[^/.]+)')
    # def update_by_code(self, request, code=None):
    #     '''Ação personalizada para atualizar CustomUser por código UUID'''
    #     return self._create_or_update(request, CustomUserUpdateByCodeSerializer, lookup_field='code', lookup_value=code)
    
    # @action(detail=False, methods=['delete'], url_path='delete_by_code/(?P<code>[^/.]+)')
    # def delete_by_code(self, request, code=None):
    #     '''Ação personalizada para excluir CustomUser por código UUID'''
    #     return self._delete(request, lookup_field='code', lookup_value=code)
    
    # @action(detail=False, methods=['get'], url_path='get_by_code/(?P<code>[^/.]+)')
    # def get_by_code(self, request, code=None):
    #     '''Ação personalizada para recuperar CustomUser por código UUID'''
    #     return self._retrieve(request, lookup_field='code', lookup_value=code)

    @action(detail=True, methods=['put', 'patch'], url_path='update_by_id')
    def update_by_id(self, request, pk=None):
        '''Ação personalizada para atualizar CustomUser por ID'''
        return self._create_or_update(request, CustomUserUpdateByIDSerializer, pk)
    
        '''  # Shell
        curl -X PUT http://127.0.0.1:8000/api/v1/consumer/custom_user/2/update_by_id/ \
            -d "email=test_update@dominio.com" \
            -d "nome=user_update" \
            -d "password=password123" \
            -u "admin@admin.com:admin"
        '''

    @action(detail=False, methods=['delete'], url_path='delete_by_id/(?P<pk>[^/.]+)')
    def delete_by_id(self, request, pk=None):
        '''
        Ação personalizada para excluir CustomUser por ID
        '''
        return self._delete(request, pk=pk)
    
        '''  # Shell
        curl -X DELETE http://127.0.0.1:8000/api/v1/consumer/custom_user/delete_by_id/2/ \
            -u "admin@admin.com:admin"
        '''
    
    @action(detail=False, methods=['get'], url_path='get_by_id/(?P<pk>[^/.]+)')
    def get_by_id(self, request, pk=None):
        '''
        Ação personalizada para recuperar CustomUser por ID
        '''
        return self._retrieve(request, pk=pk)
    
        '''  # Shell
        curl -X GET http://127.0.0.1:8000/api/v1/consumer/custom_user/get_by_id/2/ \
            -u "admin@admin.com:admin"
        '''
    
    @action(detail=False, methods=['get'], url_path='list_active')
    def list_active(self, request):
        '''
        Ação personalizada para listar usuários ativos
        '''
        return self._list(request, is_active=True)
    
        '''  # Shell
        curl -X GET http://127.0.0.1:8000/api/v1/consumer/custom_user/list_active/ \
            -u "admin@admin.com:admin"
        '''

    @action(detail=False, methods=['get'], url_path='list_inactive')
    def list_inactive(self, request):
        '''
        Ação personalizada para listar usuários inativos
        '''
        return self._list(request, is_active=False)
    
        '''  # Shell
        curl -X GET http://127.0.0.1:8000/api/v1/consumer/custom_user/list_inactive/ \
            -u "admin@admin.com:admin"
        '''

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        '''
        Ação personalizada para buscar usuários com parâmetros específicos
        '''

        query_params = request.query_params
        users = self.queryset

        # Aplica filtros baseados nos parâmetros da consulta
        for param, value in query_params.items():
            if param in [f.name for f in CustomUser._meta.get_fields()]:
                if param == 'is_active':
                    # Filtro para verificar se o usuário está ativo ou inativo
                    if value in ['true', 'True', True]:
                        users = users.filter(**{f"{param}": True})
                    else:
                        users = users.filter(**{f"{param}": False})
                else:
                    # Filtro para outros campos como nome ou email
                    users = users.filter(**{f"{param}__icontains": value})

        # Serializa a lista de usuários encontrados
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
    
        '''  # Shell
        curl -X GET "http://127.0.0.1:8000/api/v1/consumer/custom_user/search/?is_active=True&name=João" \
            -u "admin@admin.com:admin"
        '''
    
    ## Intern Functions
    
    def _create_or_update(self, request, serializer_class, pk=None, lookup_field=None, lookup_value=None):
        '''
        Função interna para criação ou atualização de um usuário
        '''

        # Busca o objeto CustomUser pelo código ou ID
        if lookup_field and lookup_value:
            instance = get_object_or_404(CustomUser, **{lookup_field: lookup_value})
        elif pk:
            instance = self.get_object()
        else:
            instance = None

        # Instancia o serializer para validação e salvamento
        serializer = serializer_class(
            instance, data=request.data, partial=request.method == 'PATCH', context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK if instance else status.HTTP_201_CREATED)

    def _delete(self, request, pk=None, lookup_field=None, lookup_value=None):
        '''
        Função interna para excluir um usuário
        '''

        # Busca o CustomUser por ID ou código
        instance = get_object_or_404(CustomUser, pk=pk) if pk else get_object_or_404(CustomUser, **{lookup_field: lookup_value})
        instance.soft_delete()  # Exclui o objeto encontrado
        return Response(status=status.HTTP_204_NO_CONTENT)  # Retorna resposta de sucesso

    def _retrieve(self, request, pk=None, lookup_field=None, lookup_value=None):
        '''
        Função interna para recuperar um usuário
        '''

        # Busca o CustomUser por ID ou código
        instance = get_object_or_404(CustomUser, pk=pk) if pk else get_object_or_404(CustomUser, **{lookup_field: lookup_value})
        serializer = self.get_serializer(instance)
        return Response(serializer.data)  # Retorna os dados do usuário encontrado

    def _list(self, request, is_active):
        '''
        Função interna para listar usuários ativos ou inativos
        '''

        queryset = CustomUser.objects.filter(is_active=is_active)  # Filtra usuários pela condição de ativo/inativo
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)  # Retorna a lista de usuários filtrados
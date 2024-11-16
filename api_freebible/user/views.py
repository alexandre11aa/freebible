from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CustomUser
from .serializers import (CustomUserSerializer,
                          CustomUserCreateWithIDSerializer,
                          CustomUserUpdateByIDSerializer)

class CustomUserViewSet(viewsets.ModelViewSet):

    ## Operacional Methods para urls

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
        # Ações de atualização usando ID
        if self.action == 'update_by_id':
            return CustomUserUpdateByIDSerializer
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
        Ação personalizada para criar um CustomUser
        '''

        # Instancia o serializer para criação de CustomUser com código UUID
        custom_user_serializer = CustomUserCreateWithIDSerializer(data=request.data)

        if custom_user_serializer.is_valid():
            custom_user = custom_user_serializer.save()  # Cria o CustomUser
            return Response({'code': custom_user.code}, status=status.HTTP_201_CREATED)  # Retorna o código UUID do usuário criado
        else:
            return Response(custom_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Retorna erros se inválido
        
        '''  # Shell
        curl -X POST http://127.0.0.1:8000/api/v1/user/custom_user/create/ \
            -d "email=test_create@test.com" \
            -d "nome=user_create" \
            -d "password=password123" \
            -u "admin@admin.com:admin"
        '''
 
    @action(detail=True, methods=['put', 'patch'], url_path='update_by_id')
    def update_by_id(self, request, pk=None):
        '''
        Ação personalizada para atualizar CustomUser por ID
        '''

        # Busca o objeto CustomUser pelo código ou ID
        if pk:
            instance = self.get_object()
        else:
            instance = None

        serializer_class = CustomUserUpdateByIDSerializer

        # Instancia o serializer para validação e salvamento
        serializer = serializer_class(
            instance, data=request.data, partial=request.method == 'PATCH', context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK if instance else status.HTTP_201_CREATED)
    
        '''  # Shell
        curl -X PUT http://127.0.0.1:8000/api/v1/user/custom_user/2/update_by_id/ \
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

        # Busca o CustomUser por ID ou código
        instance = get_object_or_404(CustomUser, pk=pk)
        instance.soft_delete()  # Exclui o objeto encontrado

        return Response(status=status.HTTP_204_NO_CONTENT)  # Retorna resposta de sucesso
    
        '''  # Shell
        curl -X DELETE http://127.0.0.1:8000/api/v1/user/custom_user/delete_by_id/2/ \
            -u "admin@admin.com:admin"
        '''
    
    @action(detail=False, methods=['get'], url_path='get_by_id/(?P<pk>[^/.]+)')
    def get_by_id(self, request, pk=None):
        '''
        Ação personalizada para recuperar CustomUser por ID
        '''

        # Busca o CustomUser por ID ou código
        instance = get_object_or_404(CustomUser, pk=pk)
        serializer = self.get_serializer(instance)

        return Response(serializer.data)  # Retorna os dados do usuário encontrado
    
        '''  # Shell
        curl -X GET http://127.0.0.1:8000/api/v1/user/custom_user/get_by_id/3/ \
            -u "admin@admin.com:admin"
        '''
    
    @action(detail=False, methods=['get'], url_path='list_active')
    def list_active(self, request):
        '''
        Ação personalizada para listar usuários ativos
        '''

        queryset = CustomUser.all_objects.filter(is_active=True)  # Filtra usuários pela condição de ativo/inativo
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)  # Retorna a lista de usuários filtrados
    
        '''  # Shell
        curl -X GET http://127.0.0.1:8000/api/v1/user/custom_user/list_active/ \
            -u "admin@admin.com:admin"
        '''

    @action(detail=False, methods=['get'], url_path='list_inactive')
    def list_inactive(self, request):
        '''
        Ação personalizada para listar usuários inativos
        '''

        queryset = CustomUser.all_objects.filter(is_active=False)  # Filtra usuários pela condição de ativo/inativo
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)  # Retorna a lista de usuários filtrados
    
        '''  # Shell
        curl -X GET http://127.0.0.1:8000/api/v1/user/custom_user/list_inactive/ \
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
        curl -X GET "http://127.0.0.1:8000/api/v1/user/custom_user/search/?is_active=True&name=João" \
            -u "admin@admin.com:admin"
        '''
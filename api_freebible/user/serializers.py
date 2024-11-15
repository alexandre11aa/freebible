from rest_framework import serializers
from .models import CustomUser

# Serializer base para CustomUser
class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer principal para manipulação geral dos campos do modelo CustomUser.
    """

    class Meta:
        model = CustomUser
        fields = (
            'id',                # ID do usuário (gerado automaticamente pelo Django)
            'code',              # Código UUID gerado automaticamente para o usuário
            'nome',              # Nome do colaborador
            'email',             # Email do colaborador
            'is_staff',          # Indica se o usuário tem privilégios de "staff"
            'is_superuser',      # Indica se o usuário é um superusuário (admin)
            'created_at',        # Data de criação do registro
            'updated_at',        # Data da última atualização do registro
            'deleted_at',        # Data de exclusão lógica (soft delete)
            'is_active'          # Indica se o registro está ativo ou não (soft delete)
        )

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value


# Serializer para criação de CustomUser com UUID code
class CustomUserCreateWithCodeSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de um novo CustomUser utilizando um código UUID como campo de referência.
    """
    
    class Meta:
        model = CustomUser
        fields = ('code', 'nome', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

# Serializer para atualização de CustomUser usando o código UUID
class CustomUserUpdateByCodeSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de CustomUser utilizando o código UUID.
    """
    
    class Meta:
        model = CustomUser
        fields = ('code', 'nome', 'email', 'password')

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

# Serializer para criação de CustomUser utilizando o ID
class CustomUserCreateWithIDSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de CustomUser utilizando o ID.
    """
    
    class Meta:
        model = CustomUser
        fields = ('id', 'nome', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


# Serializer para atualização de CustomUser usando o ID
class CustomUserUpdateByIDSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de CustomUser utilizando o ID.
    """
    
    class Meta:
        model = CustomUser
        fields = ('id', 'nome', 'email', 'password')

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
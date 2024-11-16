from rest_framework import serializers
from bible.models import Capitulo

# Serializer base para manipulação geral do modelo Capitulo
class CapituloSerializer(serializers.ModelSerializer):
    """
    Serializer principal para manipulação geral dos campos do modelo Capitulo.
    """
    class Meta:
        model = Capitulo
        fields = (
            'id',                # ID do registro
            'livro',
            'autor',
            'numero',
            'created_at',        # Data de criação (herdado do BaseModel)
            'updated_at',        # Data de última atualização (herdado do BaseModel)
            'deleted_at',        # Data de exclusão lógica (herdado do BaseModel)
            'is_active'          # Indica se está ativo ou excluído logicamente
        )

# Serializer para criação de uma versão da Bíblia
class CapituloCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de uma versão da Bíblia.
    """
    class Meta:
        model = Capitulo
        fields = ('livro', 'autor', 'numero')  # Somente campos necessários para criação

    def create(self, validated_data):
        """
        Método de criação customizado, se necessário.
        """
        chapter = Capitulo.objects.create(**validated_data)
        return chapter

# Serializer para atualização de uma versão da Bíblia
class CapituloUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de uma versão da Bíblia.
    """
    class Meta:
        model = Capitulo
        fields = ('livro', 'autor', 'numero')  # Campos que podem ser atualizados

    def update(self, instance, validated_data):
        """
        Atualiza os dados de um registro existente.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
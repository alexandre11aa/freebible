from rest_framework import serializers
from bible.models import Livro

# Serializer base para manipulação geral do modelo Livro
class LivroSerializer(serializers.ModelSerializer):
    """
    Serializer principal para manipulação geral dos campos do modelo Livro.
    """
    class Meta:
        model = Livro
        fields = (
            'id',                # ID do registro
            'biblia',
            'livro',
            'testamento',
            'created_at',        # Data de criação (herdado do BaseModel)
            'updated_at',        # Data de última atualização (herdado do BaseModel)
            'deleted_at',        # Data de exclusão lógica (herdado do BaseModel)
            'is_active'          # Indica se está ativo ou excluído logicamente
        )

# Serializer para criação de uma versão da Bíblia
class LivroCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de uma versão da Bíblia.
    """
    class Meta:
        model = Livro
        fields = ('biblia', 'livro', 'testamento')  # Somente campos necessários para criação

    def create(self, validated_data):
        """
        Método de criação customizado, se necessário.
        """
        livro = Livro.objects.create(**validated_data)
        return livro

# Serializer para atualização de uma versão da Bíblia
class LivroUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de uma versão da Bíblia.
    """
    class Meta:
        model = Livro
        fields = ('biblia', 'livro', 'testamento')  # Campos que podem ser atualizados

    def update(self, instance, validated_data):
        """
        Atualiza os dados de um registro existente.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
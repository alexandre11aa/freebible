from rest_framework import serializers
from bible.models import Versiculo

# Serializer base para manipulação geral do modelo Versiculo
class VersiculoSerializer(serializers.ModelSerializer):
    """
    Serializer principal para manipulação geral dos campos do modelo Versiculo.
    """
    class Meta:
        model = Versiculo
        fields = (
            'id',                # ID do registro
            'capitulo',
            'numero',
            'versiculo',
            'created_at',        # Data de criação (herdado do BaseModel)
            'updated_at',        # Data de última atualização (herdado do BaseModel)
            'deleted_at',        # Data de exclusão lógica (herdado do BaseModel)
            'is_active'          # Indica se está ativo ou excluído logicamente
        )

# Serializer para criação de uma versão da Bíblia
class VersiculoCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de uma versão da Bíblia.
    """
    class Meta:
        model = Versiculo
        fields = ('capitulo', 'numero', 'versiculo')  # Somente campos necessários para criação

    def create(self, validated_data):
        """
        Método de criação customizado, se necessário.
        """
        versicle = Versiculo.objects.create(**validated_data)
        return versicle

# Serializer para atualização de uma versão da Bíblia
class VersiculoUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de uma versão da Bíblia.
    """
    class Meta:
        model = Versiculo
        fields = ('capitulo', 'numero', 'versiculo')  # Campos que podem ser atualizados

    def update(self, instance, validated_data):
        """
        Atualiza os dados de um registro existente.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
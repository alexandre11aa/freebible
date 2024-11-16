from rest_framework import serializers
from bible.models import Biblia

# Serializer base para manipulação geral do modelo Biblia
class BibliaSerializer(serializers.ModelSerializer):
    """
    Serializer principal para manipulação geral dos campos do modelo Biblia.
    """
    class Meta:
        model = Biblia
        fields = (
            'id',                # ID do registro
            'code',              # Código UUID gerado automaticamente
            'lingua',            # Idioma da versão da Bíblia
            'versao',            # Versão ou autor da Bíblia
            'created_at',        # Data de criação (herdado do BaseModel)
            'updated_at',        # Data de última atualização (herdado do BaseModel)
            'deleted_at',        # Data de exclusão lógica (herdado do BaseModel)
            'is_active'          # Indica se está ativo ou excluído logicamente
        )

# Serializer para criação de uma versão da Bíblia
class BibliaCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de uma versão da Bíblia.
    """
    class Meta:
        model = Biblia
        fields = ('lingua', 'versao')  # Somente campos necessários para criação

    def create(self, validated_data):
        """
        Método de criação customizado, se necessário.
        """
        biblia = Biblia.objects.create(**validated_data)
        return biblia

# Serializer para atualização de uma versão da Bíblia
class BibliaUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de uma versão da Bíblia.
    """
    class Meta:
        model = Biblia
        fields = ('lingua', 'versao')  # Campos que podem ser atualizados

    def update(self, instance, validated_data):
        """
        Atualiza os dados de um registro existente.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
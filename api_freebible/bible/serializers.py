from rest_framework import serializers
from .models import Biblia, Livro, Capitulo, Versiculo

class BibliaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biblia
        fields = '__all__'

class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        fields = '__all__'

class CapituloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capitulo
        fields = '__all__'

class VersiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Versiculo
        fields = '__all__'
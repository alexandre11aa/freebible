from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Biblia, Livro, Capitulo, Versiculo
from .serializers import BibliaSerializer, LivroSerializer, CapituloSerializer, VersiculoSerializer

class BibliaListCreate(generics.ListCreateAPIView):
    queryset = Biblia.objects.all()
    serializer_class = BibliaSerializer
    permission_classes = [IsAuthenticated]

class LivroListCreate(generics.ListCreateAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    permission_classes = [IsAuthenticated]

class CapituloListCreate(generics.ListCreateAPIView):
    queryset = Capitulo.objects.all()
    serializer_class = CapituloSerializer
    permission_classes = [IsAuthenticated]

class VersiculoListCreate(generics.ListCreateAPIView):
    queryset = Versiculo.objects.all()
    serializer_class = VersiculoSerializer
    permission_classes = [IsAuthenticated]
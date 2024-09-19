from django.urls import path
from .views import BibliaListCreate, LivroListCreate, CapituloListCreate, VersiculoListCreate

urlpatterns = [
    path('biblia/', BibliaListCreate.as_view(), name='biblia-list-create'),
    path('livro/', LivroListCreate.as_view(), name='livro-list-create'),
    path('capitulo/', CapituloListCreate.as_view(), name='capitulo-list-create'),
    path('versiculo/', VersiculoListCreate.as_view(), name='versiculo-list-create'),
]
import os
import django

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ramal_unifip.settings')
django.setup()

# Registrando Dados
from django.core.exceptions import ObjectDoesNotExist
from bible.models import Biblia, Livro, Capitulo, Versiculo

def create_bible_version_if_not_exists(lingua, versao, default=False):
    '''
    Registra nova versão da Bíblia ao iniciar container caso ela não exista
    '''
    
    # Tenta obter o colaborador pelo email
    try:
        existing_bible_version = Biblia.objects.get(lingua=lingua, versao=versao, default=False)

        if default == True:
            print('Versão padrão da Bíblia já está registrada.')

        return existing_bible_version

    # Se não existir, cria um novo colaborador e o usuário associado
    except ObjectDoesNotExist:
        bible = Biblia.objects.create(
            lingua=lingua,
            versao=versao,
        )
        bible.save()

        if default == True:
            print('Versão padrão da Bíblia foi registrada.')

        return bible

def create_book_if_not_exists(biblia, livro, testamento, default=False):
    '''
    Registra novo livro da Bíblia ao iniciar container caso ele não exista
    '''
    
    # Tenta obter o colaborador pelo email
    try:
        existing_book = Livro.objects.get(biblia=biblia, livro=livro)

        if default == True:
            print('Livro padrão da Bíblia já está registrado.')

        return existing_book

    # Se não existir, cria um novo colaborador e o usuário associado
    except ObjectDoesNotExist:
        book = Livro.objects.create(
            biblia=biblia,
            livro=livro,
            testamento=testamento,
        )
        book.save()

        if default == True:
            print('Livro padrão da Bíblia foi registrado.')

        return book
    
def create_chapter_if_not_exists(livro, autor, numero, default=False):
    '''
    Registra novo capítulo da Bíblia ao iniciar container caso ele não exista
    '''
    
    # Tenta obter o colaborador pelo email
    try:
        existing_chapter = Capitulo.objects.get(livro=livro, autor=autor, numero=numero)

        if default == True:
            print('Capítulo padrão da Bíblia já está registrado.')

        return existing_chapter

    # Se não existir, cria um novo colaborador e o usuário associado
    except ObjectDoesNotExist:
        chapter = Capitulo.objects.create(
            livro=livro,
            autor=autor,
            numero=numero,
        )
        chapter.save()

        if default == True:
            print('Capítulo padrão da Bíblia foi registrado.')

        return chapter
    
def create_versicle_if_not_exists(capitulo, numero, versiculo, default=False):
    '''
    Registra novo versículo da Bíblia ao iniciar container caso ele não exista
    '''
    
    # Tenta obter o colaborador pelo email
    try:
        existing_versicle = Versiculo.objects.get(capitulo=capitulo, numero=numero, versiculo=versiculo)

        if default == True:
            print('Versículo padrão da Bíblia já está registrado.')

        return existing_versicle

    # Se não existir, cria um novo colaborador e o usuário associado
    except ObjectDoesNotExist:
        versicle = Versiculo.objects.create(
            capitulo=capitulo, 
            numero=numero, 
            versiculo=versiculo,
        )
        versicle.save()

        if default == True:
            print('Versículo padrão da Bíblia foi registrado.')

        return versicle

# Registrando versão de Bíblia
biblia_pt = create_bible_version_if_not_exists(
    lingua='PT',
    versao='Almeida',
    default=True
)

# Registrando livro da bíblia
livro_genesis = create_book_if_not_exists(
    biblia=biblia_pt,
    livro='GN',
    testamento='V',
    default=True
)

# Registrando capítulo da bíblia
capitulo_1_genesis = create_chapter_if_not_exists(
    livro=livro_genesis, 
    autor='Moisés', 
    numero=1,
    default=True
)

# Registrando capítulo da bíblia
versiculo_1 = create_versicle_if_not_exists(
    capitulo=capitulo_1_genesis, 
    numero=1, 
    versiculo='No princípio, criou Deus os céus e a terra.',
    default=True
)

# Registrando capítulo da bíblia
versiculo_2 = create_versicle_if_not_exists(
    capitulo=capitulo_1_genesis, 
    numero=2, 
    versiculo='E a terra era sem forma e vazia; e havia trevas sobre a face do abismo.',
    default=True
)

exit()
import os
import django

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ramal_unifip.settings')
django.setup()

# Registrando Dados
from django.core.exceptions import ObjectDoesNotExist
from user.models import CustomUser

def create_superuser_if_not_exists(nome, email, password):
    '''
    Cria superusuário ao iniciar container caso ele não exista
    '''
    
    # Tenta obter o colaborador pelo email
    try:
        existing_colaborador = CustomUser.objects.get(email=email)

        print('Admin default ativo.')

        return existing_colaborador

    # Se não existir, cria um novo colaborador e o usuário associado
    except ObjectDoesNotExist:
        user = CustomUser.objects.create_superuser(
            nome=nome,
            email=email,
            password=password,
        )
        user.save()

        print('Admin default ativado.')

        return user

# Criando colaboradores
superuser = create_superuser_if_not_exists(
    nome='admin',
    email='admin@admin.com',
    password='admin',
)

exit()
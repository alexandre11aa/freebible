import uuid

from django.db import models
from user.models import BaseModel


class Biblia(BaseModel):

    LINGUA_CHOICES = [
        ('PT', 'Português'),
        ('EN', 'Inglês'),
    ]

    code = models.UUIDField("Código uuid4", default=uuid.uuid4, editable=False)
    lingua = models.CharField('Linguagem', max_length=2, choices=LINGUA_CHOICES)
    versao = models.CharField('Autor', max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.versao}, {self.lingua}'
    

class Livro(BaseModel):

    biblia = models.ForeignKey(Biblia, on_delete=models.CASCADE, verbose_name='Bíblia')

    LIVRO_CHOICES = [

        # Livros do Antigo Testamento

        ('GN', 'Gênesis'),              ('EX', 'Êxodo'),                ('LV', 'Levítico'),     ('NM', 'Números'),
        ('DT', 'Deuteronômio'),         ('JS', 'Josué'),                ('JZ', 'Juízes'),       ('RT', 'Rute'),
        ('1SM', '1 Samuel'),            ('2SM', '2 Samuel'),            ('1RS', '1 Reis'),      ('2RS', '2 Reis'),
        ('1CR', '1 Crônicas'),          ('2CR', '2 Crônicas'),          ('ED', 'Esdras'),       ('NE', 'Neemias'),
        ('ET', 'Ester'),                ('JB', 'Jó'),                   ('SL', 'Salmos'),       ('PV', 'Provérbios'),
        ('EC', 'Eclesiastes'),          ('CT', 'Cânticos de Salomão'),  ('IS', 'Isaías'),       ('JR', 'Jeremias'),
        ('LM', 'Lamentações'),          ('EZ', 'Ezequiel'),             ('DN', 'Daniel'),       ('OS', 'Oséias'),
        ('JL', 'Joel'),                 ('AM', 'Amós'),                 ('OB', 'Obadias'),      ('JN', 'Jonas'),
        ('MQ', 'Miquéias'),             ('NA', 'Naum'),                 ('HC', 'Habacuque'),    ('SF', 'Sofonias'),
        ('AG', 'Ageu'),                 ('ZC', 'Zacarias'),             ('ML', 'Malaquias'),

        # Livros do Novo Testamento

        ('MT', 'Mateus'),               ('MC', 'Marcos'),               ('LC', 'Lucas'),        ('JO', 'João'),
        ('AT', 'Atos'),                 ('RM', 'Romanos'),              ('1CO', '1 Coríntios'), ('2CO', '2 Coríntios'),
        ('GL', 'Gálatas'),              ('EF', 'Efésios'),              ('FP', 'Filipenses'),   ('CL', 'Colossenses'),
        ('1TS', '1 Tessalonicenses'),   ('2TS', '2 Tessalonicenses'),   ('1TM', '1 Timóteo'),   ('2TM', '2 Timóteo'),
        ('TT', 'Tito'),                 ('FM', 'Filemom'),              ('HB', 'Hebreus'),      ('TG', 'Tiago'),
        ('1PE', '1 Pedro'),             ('2PE', '2 Pedro'),             ('1JO', '1 João'),      ('2JO', '2 João'),
        ('3JO', '3 João'),              ('JD', 'Judas'),                ('AP', 'Apocalipse'),
    ]


    TESTAMENTO_CHOICES = [
        ('N', 'Novo'),
        ('V', 'Velho'),
    ]

    livro = models.CharField('Livro', max_length=3, choices=LIVRO_CHOICES)
    testamento = models.CharField('Testamento', max_length=1, choices=TESTAMENTO_CHOICES)

    def __str__(self):
        return f'{self.biblia}, {self.livro}'
  

class Capitulo(BaseModel):

    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, verbose_name='Livro')
    autor = models.CharField('Autor do Capítulo', max_length=100, null=True, blank=True)
    numero = models.PositiveIntegerField('Número do Capítulo')

    def __str__(self):
        return f'{self.livro}, {self.numero}'

class Versiculo(BaseModel):

    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE, verbose_name='Capítulo')
    numero = models.PositiveIntegerField('Número do Versículo')
    versiculo = models.TextField('Versículo', null=True, blank=True)

    def __str__(self):
        return f'{self.capitulo}, {self.numero}'
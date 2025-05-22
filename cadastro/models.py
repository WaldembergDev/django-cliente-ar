import uuid
from django.db import models
from django.core.validators import MinValueValidator

class StatusEnum(models.TextChoices):
    PENDENTE = 'Pendente'
    ANDAMENTO = 'Andamento'
    CONCLUIDO = 'Concluido'


class Endereco(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cep = models.CharField(max_length=10, null=True, blank=True)
    logradouro = models.CharField(max_length=120)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=30, null=True, blank=True)
    bairro = models.CharField(max_length=30)
    municipio = models.CharField(max_length=30)
    
class Ambiente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    possui_ar_condicionado = models.BooleanField()
    area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantidade_maquinas = models.IntegerField(validators=[MinValueValidator(1)])
    observacoes = models.TextField(null=True, blank=True)

# Create your models here.
class Cliente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome_razao_social = models.CharField(max_length=120)
    nome_fantasia = models.CharField(max_length=120, null=True, blank=True)
    cpf_cnpj = models.CharField(max_length=18, null=True, blank=True)
    contato = models.CharField(max_length=50)
    telefone_1 = models.CharField(max_length=40)
    telefone_2 = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=120, null=True, blank=True)
    status = models.CharField(
        max_length=15,
        choices=StatusEnum.choices,
        default=StatusEnum.PENDENTE
        )
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE)
    ambiente = models.OneToOneField(Ambiente, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_razao_social
    
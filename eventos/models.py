# eventos/models.py (COPIAR E COLAR TUDO)

from django.db import models
from django.contrib.auth.models import User


class Evento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventos')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    local = models.CharField(max_length=200, default='Local não definido')
    numero_pessoas = models.IntegerField(default=0)
    data_hora = models.DateTimeField()
    duracao = models.CharField(max_length=50, default='1 hora')
    tipo = models.CharField(max_length=50, default='Geral')
    imagem = models.ImageField(upload_to='eventos_imagens/', blank=True, null=True)


    def __str__(self):
        return self.titulo
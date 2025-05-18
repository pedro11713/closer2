from django.db import models
from datetime import datetime

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    local = models.CharField(max_length=200, default='Local não definido')
    numero_pessoas = models.IntegerField(default=0)
    data_hora = models.DateTimeField(default=datetime.now)
    duracao = models.CharField(max_length=50, default='1 hora')
    tipo = models.CharField(max_length=50, default='Geral')
    imagem_url = models.URLField(blank=True)

    def __str__(self):
        return self.titulo

from django.db import models


class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    imagem_url = models.URLField()

    def __str__(self):
        return self.titulo

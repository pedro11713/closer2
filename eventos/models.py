# eventos/models.py (VERSÃO CORRIGIDA E COMPLETA)

from django.db import models
from django.contrib.auth.models import User

# --- MODELO 1: Evento ---
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


# --- MODELO 2: Participacao ---
# (Observe que está no mesmo nível de indentação que a classe Evento)
class Participacao(models.Model):
    """
    Representa a relação de um Usuário com um Evento.
    Pode ser um pedido pendente, uma participação confirmada, etc.
    """
    class Status(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        ACEITO = 'ACEITO', 'Aceito'
        REJEITADO = 'REJEITADO', 'Rejeitado'

    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="participacoes")
    participante = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participacoes_eventos")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDENTE)
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Garante que um usuário só pode se inscrever uma vez em cada evento
        unique_together = ('evento', 'participante')

    def __str__(self):
        return f"{self.participante.username} - {self.evento.titulo} ({self.get_status_display()})"


# --- MODELO 3: MensagemChat ---
# (Também no mesmo nível de indentação)
class MensagemChat(models.Model):
    """
    Representa uma única mensagem no chat de um evento.
    """
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="mensagens")
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    conteudo = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Msg de {self.autor.username} em {self.evento.titulo} @ {self.timestamp.strftime('%H:%M')}"

    class Meta:
        ordering = ['timestamp'] # Ordena as mensagens da mais antiga para a mais nova
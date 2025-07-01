# eventos/serializers.py (VERSÃO COMPLETA E CORRIGIDA)

from rest_framework import serializers
from .models import Evento, Participacao, MensagemChat
from django.contrib.auth.models import User


# Serializer auxiliar para não expor todos os dados do usuário
class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


# Serializer principal de Evento
class EventoSerializer(serializers.ModelSerializer):
    imagem_url = serializers.SerializerMethodField()

    class Meta:
        model = Evento
        fields = [
            'id', 'titulo', 'descricao', 'local', 'numero_pessoas',
            'data_hora', 'duracao', 'tipo', 'imagem', 'imagem_url', 'usuario'
        ]
        read_only_fields = ['usuario']
        extra_kwargs = {
            'imagem': {'required': False, 'allow_null': True}
        }

    def get_imagem_url(self, obj):
        request = self.context.get('request')
        if request and obj.imagem and hasattr(obj.imagem, 'url'):
            return request.build_absolute_uri(obj.imagem.url)
        return None


# Serializer de Participacao
class ParticipacaoSerializer(serializers.ModelSerializer):
    participante = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Participacao
        fields = ['id', 'evento', 'participante', 'status', 'data_solicitacao']
        read_only_fields = ['evento', 'participante', 'data_solicitacao']


# --- CORREÇÃO PRINCIPAL AQUI ---
# Serializer de MensagemChat simplificado
class MensagemChatSerializer(serializers.ModelSerializer):
    # Apenas declaramos que 'autor' deve usar o UserSimpleSerializer e é somente leitura.
    # O DRF cuida do resto, incluindo o contexto.
    autor = UserSimpleSerializer(read_only=True)

    class Meta:
        model = MensagemChat
        fields = ['id', 'evento', 'autor', 'conteudo', 'timestamp']
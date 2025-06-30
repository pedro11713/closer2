# eventos/serializers.py (VERSÃO FINAL E CORRIGIDA)

from rest_framework import serializers
from .models import Evento

class EventoSerializer(serializers.ModelSerializer):
    imagem_url = serializers.SerializerMethodField()

    class Meta:
        model = Evento
        fields = [
            'id', 'titulo', 'descricao', 'local', 'numero_pessoas',
            'data_hora', 'duracao', 'tipo', 'imagem', 'imagem_url', 'usuario'
        ]
        read_only_fields = ['usuario']

        # Define regras extras para campos específicos
        extra_kwargs = {
            'imagem': {'required': False, 'allow_null': True}
        }

    # 3. Criamos a função especial get_<nome_do_campo>.
    #    Esta função será chamada para cada evento sendo serializado.
    def get_imagem_url(self, obj):
        """
        Retorna a URL completa da imagem se ela existir.
        'obj' aqui é a instância do modelo Evento.
        """
        request = self.context.get('request')
        if obj.imagem and hasattr(obj.imagem, 'url'):
            # obj.imagem.url nos dá o caminho relativo (ex: /media/eventos_imagens/foto.jpg)
            # request.build_absolute_uri constrói a URL completa
            # (ex: http://localhost:8000/media/eventos_imagens/foto.jpg)
            return request.build_absolute_uri(obj.imagem.url)
        # Retorna None ou uma URL de placeholder se não houver imagem
        return None
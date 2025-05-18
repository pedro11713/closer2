from django.http import JsonResponse
from .models import Evento

def listar_eventos(request):
    eventos = list(Evento.objects.values())  # retorna [{id:..., titulo:..., imagem_url:...}, ...]
    return JsonResponse(eventos, safe=False)

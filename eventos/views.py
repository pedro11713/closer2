# eventos/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Evento
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from .serializers import EventoSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 1. Exige login
def listar_eventos(request):
    # 2. Busca todos os eventos E exclui aqueles cujo 'usuario' é o usuário da requisição
    eventos = Evento.objects.exclude(usuario=request.user)

    # 3. Usa o Serializer para formatar os dados (ele criará a URL completa para a imagem)
    serializer = EventoSerializer(eventos, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Nome de usuário e senha são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Este nome de usuário já existe'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, password=password)
    return Response({'message': f'Usuário {user.username} criado com sucesso'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Login realizado com sucesso', 'username': user.username})
    else:
        return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logout realizado com sucesso'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_view(request):
    # Se chegar aqui, o usuário está autenticado
    return Response({'username': request.user.username})


@ensure_csrf_cookie
def get_csrf_token(request):
    # Esta view serve apenas para o frontend obter o cookie CSRF inicial
    return JsonResponse({'detail': 'CSRF cookie set'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request):
    # --- CORREÇÃO AQUI ---
    # Passe o contexto da requisição para o serializer.
    serializer = EventoSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        serializer.save(usuario=request.user)
        # O serializer agora tem o 'request' e pode construir a 'imagem_url'
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def meus_eventos(request):
    """
    Retorna apenas os eventos criados pelo usuário que está logado.
    """
    eventos = Evento.objects.filter(usuario=request.user).order_by('-data_hora')
    serializer = EventoSerializer(eventos, many=True, context={'request': request})
    return Response(serializer.data)


# eventos/views.py (ADICIONE ESTA NOVA VIEW)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletar_evento(request, pk):
    """
    Apaga um evento. Garante que apenas o criador do evento possa apagá-lo.
    'pk' é a Primary Key (o id) do evento.
    """
    try:
        # Tenta encontrar o evento pelo ID (pk) E pelo usuário dono
        evento = Evento.objects.get(pk=pk, usuario=request.user)
    except Evento.DoesNotExist:
        # Se não encontrar, significa que o evento não existe ou não pertence ao usuário
        return Response({'error': 'Evento não encontrado ou você não tem permissão para apagar.'},
                        status=status.HTTP_404_NOT_FOUND)

    evento.delete()
    return Response({'message': 'Evento apagado com sucesso!'},
                    status=status.HTTP_204_NO_CONTENT)  # 204 significa sucesso, sem conteúdo na resposta


# Adicione esta função ao seu arquivo eventos/views.py

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def editar_evento(request, pk):
    """
    Atualiza um evento existente. PATCH permite atualizações parciais.
    """
    try:
        evento = Evento.objects.get(pk=pk, usuario=request.user)
    except Evento.DoesNotExist:
        return Response({'error': 'Evento não encontrado ou você não tem permissão para editar.'},
                        status=status.HTTP_404_NOT_FOUND)

    # partial=True permite que o serializer aceite atualizações parciais (sem todos os campos)
    serializer = EventoSerializer(instance=evento, data=request.data, partial=True, context={'request': request})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Adicione esta função ao seu arquivo eventos/views.py

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalhe_evento(request, pk):
    """
    Retorna os detalhes de um único evento.
    Usado para preencher o formulário de edição.
    """
    try:
        # Busca o evento pelo ID (pk) e garante que ele pertence ao usuário logado.
        evento = Evento.objects.get(pk=pk, usuario=request.user)
    except Evento.DoesNotExist:
        # Se não encontrar, retorna um erro 404.
        return Response({'error': 'Evento não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    # Se encontrar, serializa os dados e os retorna.
    serializer = EventoSerializer(evento, context={'request': request})
    return Response(serializer.data)
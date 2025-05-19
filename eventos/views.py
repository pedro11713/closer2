from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Evento
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


@api_view(['GET'])
def listar_eventos(request):
    eventos = list(Evento.objects.values('id', 'titulo', 'descricao', 'imagem_url'))
    return Response(eventos)


@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Invalid username/password'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, password=password)
    return Response({'message': f'User {user.username} created successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_view(request):
    print("Dados RECEBIDOSSSSS:", request.data)  # <- ADICIONE ISTO
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Logged in successfully'})
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_view(request):
    print(request.user.username)
    return Response({'username': request.user.username})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_evento(request):
    data = request.data.copy()  # Cria uma cópia mutável
    if not data.get('imagem_url'):
        data['imagem_url'] = '/logo512.png'  # Caminho padrão temporário

    serializer = EventoSerializer(data=data)
    if serializer.is_valid():
        serializer.save(usuario=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


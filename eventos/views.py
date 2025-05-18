from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Evento
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


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
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Logged in successfully'})
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

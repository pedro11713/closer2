from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from eventos.views import (
    listar_eventos, login_view, signup, logout_view,
    user_view, create_event, get_csrf_token, meus_eventos, deletar_evento, detalhe_evento,  editar_evento, solicitar_participacao, responder_solicitacao, listar_meus_chats, listar_mensagens, enviar_mensagem, listar_solicitacoes_por_evento
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/eventos/', listar_eventos),
    path('api/signup/', signup),
    path('api/login/', login_view),
    path('api/logout/', logout_view),
    path('api/user/', user_view),
    path('api/create/', create_event),
    path('get_csrf/', get_csrf_token),
    path('api/meus-eventos/', meus_eventos),
    path('api/evento/delete/<int:pk>/', deletar_evento),
    path('api/evento/edit/<int:pk>/', editar_evento),
    path('api/evento/<int:pk>/', detalhe_evento),
    path('api/evento/solicitar/<int:pk>/', solicitar_participacao),
    path('api/responder-solicitacao/<int:pk>/', responder_solicitacao),
    path('api/meus-chats/', listar_meus_chats),
    path('api/chat/<int:evento_id>/mensagens/', listar_mensagens),
    path('api/chat/<int:evento_id>/enviar/', enviar_mensagem),
    path('api/evento/<int:evento_id>/solicitacoes/', listar_solicitacoes_por_evento),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
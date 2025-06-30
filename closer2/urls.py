from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from eventos.views import (
    listar_eventos, login_view, signup, logout_view,
    user_view, create_event, get_csrf_token, meus_eventos, deletar_evento, detalhe_evento,  editar_evento
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

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
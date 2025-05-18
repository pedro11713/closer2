from django.contrib import admin
from django.urls import path
from eventos.views import listar_eventos
from eventos.views import login_view  # <- Corrigido aqui
from eventos.views import signup  # <- Corrigido aqui

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/eventos/', listar_eventos),
    path('api/signup/', signup),
    path('api/login/', login_view),


]

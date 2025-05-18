from django.contrib import admin
from django.urls import path
from eventos.views import listar_eventos
from eventos import views  # <- Corrigido aqui

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/eventos/', listar_eventos),
    path('api/signup/', views.signup),
    path('api/login&register/', views.login_view),
]

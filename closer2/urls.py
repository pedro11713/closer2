from django.contrib import admin
from django.urls import path
from eventos.views import listar_eventos, login_view, signup, logout_view, user_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/eventos/', listar_eventos),
    path('api/signup/', signup),
    path('api/login/', login_view),
    path('api/logout/', logout_view),
    path('api/user/', user_view),
]

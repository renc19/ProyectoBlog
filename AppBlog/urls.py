"""
URL configuration for ProyectoBlog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.inicio, name='Inicio'),
    path('register/', views.register, name='Register'),
    path('login/', views.login_request, name='Login'),
    path('logout', LogoutView.as_view(template_name='AppBlog/inicio.html'), name='Logout'),
    path('editarPerfil', views.editar_perfil, name="EditarPerfil"),
    path('editarAvatar', views.editar_avatar, name='EditarAvatar'),
    path('verPerfil', views.ver_perfil, name="VerPerfil"),
    path('buscar_usuarios/', views.buscar_usuarios, name='BuscarUsuarios'),
    path('perfil/<int:user_id>/', views.perfil_usuario, name='PerfilUsuario'),
    path('crearPublicacion/', views.crear_publicacion, name='CrearPublicacion')
]


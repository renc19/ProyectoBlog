from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.timesince import timesince
from .models import Avatar, Publicacion
from .forms import UserRegisterForm, UserEditForm, AvatarForm, PublicacionForm
from random import sample

# Create your views here.
def inicio(request):
    avatar = Avatar.objects.filter(user=request.user.id)
    avatar_url = avatar[0].imagen.url if avatar else ''

    publicaciones = Publicacion.objects.all()
    publicaciones_random = sample(list(publicaciones), len(publicaciones))

    avatares = Avatar.objects.all()

    return render(request, 'AppBlog/inicio.html', {'publicaciones': publicaciones_random, 'avatares': avatares, 'avatar_url':avatar_url})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            form.save()
            messages.success(request, f"Su cuenta ha sido creada correctamente.\n¡Bienvenido!")
            return redirect('Inicio')
    else:
        form = UserRegisterForm()

    return render(request, 'AppBlog/register.html', {'form':form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contra = form.cleaned_data.get('password')

            user = authenticate(username=usuario, password=contra)

            if user is not None:
                login(request, user)
                
                messages.success(request, f"¡Bienvenido {usuario}!")
                return redirect('Inicio')
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
                return redirect('Login')
        else:
            messages.error(request, "Error, formulario erroneo.")
            return redirect('Inicio')
        
    form = AuthenticationForm()

    return render(request, "AppBlog/login.html", {'form':form})

@login_required
def editar_perfil(request):
    usuario = request.user
    avatares = Avatar.objects.filter(user=request.user.id)
    avatar_url = avatares[0].imagen.url if avatares else ''

    if request.method == 'POST':
        form = UserEditForm(request.POST)

        if form.is_valid():
            info = form.cleaned_data

            usuario.email = info['email']
            usuario.password1 = info['password1']
            usuario.password2 = info['password2']

            usuario.save()

            messages.success(request, "Cambios realizados correctamente.")
            return redirect('Inicio')
    else:
        form = UserEditForm(initial={'email': usuario.email})

    return render(request, 'AppBlog/editar_perfil.html', {'form':form, 'usuario':usuario, 'avatar_url':avatar_url})

@login_required
def ver_perfil(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    avatar_url = avatares[0].imagen.url if avatares else ''

    return render(request, 'AppBlog/ver_perfil.html', {'avatar_url': avatar_url})

@login_required
def editar_avatar(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    avatar_url = avatares[0].imagen.url if avatares else ''

    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)

        if form.is_valid():
            u = User.objects.get(username=request.user)

            if avatares:
                avatares[0].delete()

            avatar = Avatar(user=u, imagen=form.cleaned_data['imagen'])
            avatar.save()

            messages.success(request, 'Avatar actualizado con éxito.')
            return redirect('VerPerfil')
    else:
        form = AvatarForm()

    return render(request, 'AppBlog/editar_avatar.html', {'form': form, 'avatar_url':avatar_url})

@csrf_protect
def buscar_usuarios(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    avatar_url = avatares[0].imagen.url if avatares else ''
    query = request.GET.get('q', '')
    usuarios = User.objects.filter(username__icontains=query)

    return render(request, 'AppBlog/buscar_usuarios.html', {'usuarios': usuarios, 'avatar_url':avatar_url})

def perfil_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    avatares = Avatar.objects.filter(user=request.user.id)
    avatar_url = avatares[0].imagen.url if avatares else ''
    user_avatares = Avatar.objects.filter(user=usuario)
    user_avatar_url = user_avatares[0].imagen.url if user_avatares else ''

    return render(request, 'AppBlog/perfil_usuario.html', {'usuario':usuario, 'avatar_url':avatar_url, 'user_avatar_url': user_avatar_url})

@login_required
def crear_publicacion(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    avatar_url = avatares[0].imagen.url if avatares else ''

    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_publicacion = form.save(commit=False)
            nueva_publicacion.autor = request.user
            nueva_publicacion.save()
            messages.success(request, "Se ha realizado la publicación.")
            return redirect('Inicio')
    else:
        form = PublicacionForm()

    return render(request, 'AppBlog/crear_publicacion.html', {'form':form, 'avatar_url':avatar_url})
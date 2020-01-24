from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login,
    update_session_auth_hash
    )
from django.contrib.auth.forms import (
    UserChangeForm, 
    UserCreationForm, 
    PasswordChangeForm
    )
from .forms import (    
    EditProfileForm,
    RegisterProfileForm,    
    ProfileForm, 
    NewMessage,   
    )
from .models import Profile, Mensagem
from .funcoes import *
from django.core.files.base import ContentFile
import datetime
import base64
#import time

# Create your views here.
def Home(request):            
    args = {}
    return render(request, 'app/home.html', args)

def Profile(request):    
    args = {'user': request.user,
            'profile': request.user.profile}
    
    return render(request, 'accounts/profile.html', args)

def Edit_profile(request):    
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()            
            messages.success(request, "Informações atualizadas com sucesso.", extra_tags='alert-success alert-dismissible')
            return redirect('app:profile')
        else:
            messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert-error alert-dismissible')               
    else:
        user_form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    args = {'user_form': user_form,
            'profile_form': profile_form}
    

    return render(request, 'accounts/edit_profile.html', args)

def Edit_profilepic(request):   
    if request.method == 'POST':     
        imagem = request.POST.get('image')             
        if imagem != '':            
            image_data = imagem
            format, imgstr = image_data.split(';base64,')
            #print("format", format)
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr))  
            file_name = "'" + request.user.username + "." + ext        
            request.user.profile.foto_perfil.save(file_name, data, save=True) # image is User's model field
        else:
            request.user.profile.ApagaFoto()
            
        return HttpResponse('')        
        
    args = {'profile': request.user.profile}                

    return render(request, 'accounts/edit_profilepic.html', args)

def Register(request):
    if request.method == 'POST':
        form = RegisterProfileForm(request.POST)
        if form.is_valid():
            form.save()            
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('app:profile')                    
    else:
        form = RegisterProfileForm()

    args = {'form': form}
    return render(request,'accounts/register.html', args)

def Change_Password(request):
    
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Informações atualizadas com sucesso.", extra_tags='alert-success alert-dismissible')
            return redirect('app:profile')        
        else:
            messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert-error alert-dismissible')               
    else:
        form = PasswordChangeForm(user=request.user)

    args = {'form': form}    
    return render(request, 'accounts/change_password.html', args)

def Inbox(request):                            
    reg_pag           = request.GET.get('reg_pag', 10)        
    ordenar           = request.GET.get('ordenar', '-dt_mensagem')        
    buscar            = request.GET.get('buscar', '')            
    
    filtro_url = '?reg_pag=' + str(reg_pag) + '&ordenar=' + str(ordenar) + '&buscar=' + str(buscar)
    filtro = {'url': filtro_url,              
              'pag': reg_pag,              
              'ordenar': ordenar,
              'buscar': buscar,
              }    

    mensagem = Mensagem.objects.filter(destinatario=request.user).filter(mensagem__contains=buscar).order_by(ordenar)               

    page    = request.GET.get('page', 1)    

    paginator = Paginator(mensagem, reg_pag)
    try:
        mensagens = paginator.page(page)
    except PageNotAnInteger:
        mensagens = paginator.page(1)
    except EmptyPage:
        mensagens = paginator.page(paginator.num_pages)    

    args = {'mensagem': mensagens, 'filtro': filtro}
    

    return render(request, 'app/inbox.html', args)

def Msg_View(request, pk):        
    mensagem = get_object_or_404(Mensagem, pk=pk)
    mensagem.Lida(True)
    args = {'msg': mensagem}
    
    return render(request, 'app/message_detail.html', args)

def New_Msg(request):    
    if request.method == 'POST':
        form = NewMessage(request.POST)        
        if form.is_valid():            
            if "todos" in request.POST:
                usuarios = User.objects.all()
                mensagem = form.save(commit=False)                        
                for destin in usuarios:                    
                    Mensagem.objects.create(destinatario=destin, 
                                            remetente=request.user,
                                            assunto=mensagem.assunto, 
                                            mensagem=mensagem.mensagem,
                                            dt_mensagem=timezone.now())

                messages.success(request, "Mensagens enviadas com sucesso.", extra_tags='alert-success alert-dismissible')
                return redirect('app:inbox')        
            else:
                mensagem = form.save(commit=False)    
                mensagem.dt_mensagem = timezone.now()
                mensagem.remetente = request.user
                mensagem.save()
                messages.success(request, "Mensagem enviada com sucesso.", extra_tags='alert-success alert-dismissible')
                return redirect('app:inbox')            
    else:
        form = NewMessage()


    args = {'form': form}

    return render(request, 'app/new_message.html', args)

def Del_Msg(request):    
    if request.POST and request.is_ajax():        
        if request.POST.getlist('msgs_list[]'):
            msg_list = request.POST.getlist('msgs_list[]')            
            for i in msg_list:
                mensagem = Mensagem.objects.get(pk=i)
                mensagem.delete()            
            messages.success(request, "Mensagens excluidas com sucesso.", extra_tags='alert-success alert-dismissible')            
        else:
            messages.error(request, "Nenhuma mensagem selecionada.", extra_tags='alert-error alert-dismissible')               

    return HttpResponse('')

def Read_Msg(request):    
    if request.POST and request.is_ajax():        
        if request.POST.getlist('msgs_list[]'):
            msg_list = request.POST.getlist('msgs_list[]')            
            for i in msg_list:
                mensagem = Mensagem.objects.get(pk=i)
                mensagem.Lida(True)         
            messages.success(request, "Mensagens alteradas com sucesso.", extra_tags='alert-success alert-dismissible')            
        else:
            messages.error(request, "Nenhuma mensagem selecionada.", extra_tags='alert-error alert-dismissible')               

    return HttpResponse('')

def Unread_Msg(request):    
    if request.POST and request.is_ajax():        
        if request.POST.getlist('msgs_list[]'):
            msg_list = request.POST.getlist('msgs_list[]')            
            for i in msg_list:
                mensagem = Mensagem.objects.get(pk=i)
                mensagem.Lida(False)         
            messages.success(request, "Mensagens alteradas com sucesso.", extra_tags='alert-success alert-dismissible')            
        else:
            messages.error(request, "Nenhuma mensagem selecionada.", extra_tags='alert-error alert-dismissible')               

    return HttpResponse('')

def Side_Menu(request):
    if request.session.get('menu_aberto') != '':
        request.session['menu_aberto'] = not(request.session.get('menu_aberto'))

    return HttpResponse('')
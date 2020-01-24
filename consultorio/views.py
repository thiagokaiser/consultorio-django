from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from .forms import PacienteFormView, ConsultaFormView
from django.contrib import messages
from .models import Paciente, Consulta
from django.core.serializers import serialize
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date, datetime, timedelta

# Create your views here.

def home(request):
    args = {}
    return render(request, 'consultorio/home.html', args)

def newPaciente(request):
    if request.method == 'POST':
        form = PacienteFormView(request.POST)
        if form.is_valid():            
            paciente = form.save(commit=False)
            paciente.usuario = request.user
            paciente.save()
            messages.success(request, "Informações atualizadas com sucesso.", extra_tags='alert-success alert-dismissible')
            return redirect('consultorio:home')        
        else:
            messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert-error alert-dismissible')               
    else:
        form = PacienteFormView()

    args = {'form': form}        
    return render(request, 'consultorio/newPaciente.html', args)

def editPaciente(request, pk):
    paciente = get_object_or_404(Paciente,pk=pk)

    if request.method == 'POST':
        form = PacienteFormView(request.POST, instance=paciente)
        if form.is_valid():
            form.save()            
            messages.success(request, "Informações atualizadas com sucesso.", extra_tags='alert-success alert-dismissible')
            return redirect('consultorio:listPaciente')        
        else:
            messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert-error alert-dismissible')               
    else:
        form = PacienteFormView(instance=paciente)

    args = {'form': form}        
    return render(request, 'consultorio/newPaciente.html', args)

def detailPaciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    args = {'paciente': paciente}
    
    return render(request, 'consultorio/detailPaciente.html', args)

def listPaciente(request):
    
    reg_pag = request.GET.get('reg_pag', 5)            
    nome    = request.GET.get('nome', '')            
    page    = request.GET.get('page', 1)    
    
    filtro_url = '?reg_pag=' + str(reg_pag) + '&nome=' + str(nome)

    filtro = {'url': filtro_url,              
              'pag': reg_pag,                            
              'nome': nome}    

    pacientes = Paciente.objects.filter(nome__contains=nome).order_by('nome')

    for pacient in pacientes:
        today = date.today() 
        age = today.year - pacient.dt_nascimento.year - ((today.month, today.day) < (pacient.dt_nascimento.month, pacient.dt_nascimento.day)) 
        pacient.idade = age
        
    paginator = Paginator(pacientes, reg_pag)
    try:
        pacientespag = paginator.page(page)
    except PageNotAnInteger:
        pacientespag = paginator.page(1)
    except EmptyPage:
        pacientespag = paginator.page(paginator.num_pages)
    
    args = {'pacientes': pacientespag, 'filtro': filtro}
    
    return render(request, 'consultorio/listPaciente.html', args)

def viewPaciente(request):
    if request.is_ajax():
        chave = request.POST.get('chave')
        paciente = Paciente.objects.get(pk=chave)        
        retorno = serialize('json', [paciente])        
        
        return HttpResponse(retorno)
		
def viewConsulta(request):
    if request.is_ajax():
        chave = request.POST.get('chave')        
        consulta = Consulta.objects.filter(paciente_id=chave).values()
        return JsonResponse(list(consulta), safe=False)	

def newConsulta(request, pk):
    paciente = Paciente.objects.get(pk=pk)
    if request.method == 'POST':
        form = ConsultaFormView(request.POST)
        if form.is_valid():            
            consulta = form.save(commit=False)
            consulta.usuario = request.user            
            consulta.paciente = paciente
            consulta.save()
            messages.success(request, "Informações atualizadas com sucesso.", extra_tags='alert-success alert-dismissible')
            return redirect('consultorio:home')        
        else:
            messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert-error alert-dismissible')               
    else:
        form = ConsultaFormView()

    args = {'form': form, 'paciente': paciente}        
    return render(request, 'consultorio/newConsulta.html', args)

def editConsulta(request, pk):

    consulta = get_object_or_404(Consulta,pk=pk)
    paciente = Paciente.objects.get(pk=consulta.paciente.pk)

    if request.method == 'POST':
        form = ConsultaFormView(request.POST, instance=consulta)
        if form.is_valid():
            form.save()            
            messages.success(request, "Informações atualizadas com sucesso.", extra_tags='alert-success alert-dismissible')
            return redirect('consultorio:listPaciente')        
        else:
            messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert-error alert-dismissible')               
    else:
        form = ConsultaFormView(instance=consulta)

    args = {'form': form, 'paciente': paciente}        
    return render(request, 'consultorio/newConsulta.html', args)

def detailConsulta(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    args = {'consulta': consulta}
    
    return render(request, 'consultorio/detailConsulta.html', args)

from django import forms
from .models import Paciente, Consulta
from django.forms.widgets import TextInput

class PacienteFormView(forms.ModelForm):
	class Meta:
		model = Paciente
		fields = (
				'nome',
				'cidade', 
				'estado',
				'dt_nascimento' 		  
		)
		widgets = {
			'dt_nascimento': TextInput(attrs={'type': 'date'}),
		}	

class ConsultaFormView(forms.ModelForm):
	class Meta:
		model = Consulta
		fields = (
				'dt_consulta',
				'diagnostico',
				'conduta', 
				'cid'				
		)		
		widgets = {
			'dt_consulta': TextInput(attrs={'type': 'date'}),
		}
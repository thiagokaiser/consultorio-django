from django import forms
from .models import Profile, Mensagem
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .fields import RestrictedFileField
from django.forms.widgets import TextInput

class EditProfileForm(UserChangeForm):
	password = ReadOnlyPasswordHashField()	
	class Meta:
		model = User
		fields = (
		'first_name',
		'last_name',
		'email',		
		'password'		
		)	

	def clean_email(self):		
		email = self.cleaned_data['email']
		usuario	= User.objects.filter(email=email)
		usuario = usuario.exclude(pk=self.instance.pk)
		if usuario.exists() == True:
			raise ValidationError("Email já cadastrado para outro usuário.")
		if email == '':
			raise ValidationError("Email é obrigatório.")
		return email

	def clean_first_name(self):
		first_name = self.cleaned_data['first_name']
		if first_name == '':
			raise ValidationError("Nome é obrigatório.")
		return first_name

	def clean_last_name(self):
		last_name = self.cleaned_data['last_name']
		if last_name == '':
			raise ValidationError("Nome é obrigatório.")
		return last_name


class RegisterProfileForm(UserCreationForm):
	email = forms.EmailField(required=True)	
	class Meta:
		model = User
		fields = (
		'username',
		'email',
		'first_name',
		'last_name',
		'password1',
		'password2'
		)		

	def save(self, commit=True):
		user = super(RegisterProfileForm, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']

		if commit:
			user.save()

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists() == True:
			raise ValidationError("Email já cadastrado para outro usuário.")			
		return email

class ProfileForm(forms.ModelForm):
	"""foto_perfil = RestrictedFileField(content_types=['image/jpeg','image/png', 'application/pdf'],
									  max_upload_size=1600000, 
									  required=False,									  
									  help_text='Arquivos válidos: jpg, png, pdf. Tamanho máximo: 1.5mb')"""
	class Meta:
		model = Profile
		fields = (			
			'dt_nascimento',
			'cidade',
			'estado',			
			'layoutskin',
			'descricao')
		widgets = {
            'dt_nascimento': TextInput(attrs={'type': 'date'}),
        }

class MensagemFormView(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ('remetente',
        		  'assunto', 
        		  'mensagem',
        		  'dt_mensagem' 		  
        		  )

class NewMessage(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ('destinatario',
        		  'assunto', 
        		  'mensagem',        		  
        		  )
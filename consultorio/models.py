from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Paciente(models.Model):
    usuario			= models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    nome     		= models.CharField(max_length=100, blank=True)
    cidade 			= models.CharField(max_length=30, blank=True)
    estado 			= models.CharField(max_length=2, blank=True)
    dt_nascimento 	= models.DateField(null=True, blank=True)
    

class Consulta(models.Model):
    usuario 		= models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    paciente        = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    diagnostico     = models.TextField(max_length=500, blank=True)
    conduta         = models.TextField(max_length=500, blank=True)
    cid             = models.CharField(max_length=30, blank=True)
    dt_consulta     = models.DateField(null=True, blank=True)

    
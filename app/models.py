from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

class Profile(models.Model):
    user 			= models.OneToOneField(User, on_delete=models.CASCADE)
    descricao 		= models.TextField(max_length=500, blank=True)
    cidade 			= models.CharField(max_length=30, blank=True)
    estado 			= models.CharField(max_length=2, blank=True)
    dt_nascimento 	= models.DateField(null=True, blank=True)
    foto_perfil     = models.FileField(upload_to='perfil/', blank=True, null=True)
    layoutskin      = models.ForeignKey('LayoutSkin', on_delete=models.SET_DEFAULT, default=1)

    def ApagaFoto(self):        
        self.foto_perfil = None
        self.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

##########  deletar foto do perfil antiga ##########
@receiver(models.signals.post_delete, sender=Profile)
def delete_file_on_del_profile(sender, instance, **kwargs):    
    if instance.foto_perfil:
        if os.path.isfile(instance.foto_perfil.path):
            os.remove(instance.foto_perfil.path)

@receiver(models.signals.pre_save, sender=Profile)
def delete_file_on_change_profile(sender, instance, **kwargs):    
    if not instance.pk:
        return False

    try:
        old_file = Profile.objects.get(pk=instance.pk).foto_perfil
    except Profile.DoesNotExist:
        return False

    new_file = instance.foto_perfil    
    if not old_file == new_file:
        if old_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
######################################################

class Mensagem(models.Model):
    destinatario	= models.ForeignKey(User, on_delete=models.CASCADE)
    remetente  		= models.CharField(max_length=30, blank=True)    
    assunto         = models.CharField(max_length=30, blank=True)
    mensagem   		= models.TextField(max_length=500, blank=True)
    dt_mensagem 	= models.DateTimeField(null=True, blank=True)
    lida            = models.BooleanField(default=False)

    def Lida(self, param):
        self.lida = param
        self.save()

    def __str__(self):
        return self.assunto


class LayoutSkin(models.Model):
    descricao       = models.TextField(max_length=40, blank=True)
    nome_css        = models.TextField(max_length=40, blank=True)
    def __str__(self):
        return self.descricao

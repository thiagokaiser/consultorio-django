from .models import Mensagem
from django.contrib.auth.models import User

def base_html(request):
	#import pdb; pdb.set_trace()
	args = {}
	
	if request.user.username != '':	
		num_msgs = Mensagem.objects.filter(lida=False).filter(destinatario=request.user).count()
		msgs = Mensagem.objects.filter(destinatario=request.user).order_by('-dt_mensagem') [:5]			
		for i in msgs:
			remetente = User.objects.get(username=i.remetente)
			if remetente.profile.foto_perfil:
				i.foto = remetente.profile.foto_perfil.url			
		args = {'num_msgs': num_msgs,
				'msgs': msgs}
				
	return args
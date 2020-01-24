from django.contrib.auth.models import User
from financ.models import Importacao

user  = User.objects.get(username='kaiserz')

Importacao.objects.create(
	descricao='Hist Mobills',
	dt_import='2018-09-05',
	usuario=user
	)
import csv
from django.contrib.auth.models import User
from financ.models import Despesa, Categoria, Importacao

with open('financ/scripts/despesas-all.csv', encoding='utf-8') as csvfile:
	reader = csv.DictReader(csvfile, delimiter=';')

	for row in reader:
		
		categ = Categoria.objects.get(descricao=row['Categoria'])
		user  = User.objects.get(username='kaiserz')
		importacao = Importacao.objects.get(descricao='Hist Mobills')

		valor = row['Valor'].replace('R$','')
		valor = valor.replace('.','')
		valor = valor.replace(',','.')

		dia = row['Data'][:2]
		mes = row['Data'][3:5]
		ano = row['Data'][6:10]

		data = ano + '-' + mes + '-' + dia
		
		#ignorar mes de agosto e setembro
		if (mes == '08' or mes == '09') and ano == '2018':
			print(data)
		else:		
			Despesa.objects.create(valor		  = valor,
								   descricao	  = row['descricao'],
								   dt_vencimento  = data,
								   categoria	  = categ,
								   pago		      = True,
								   fixa           = False,							   
								   usuario        = user,							   
								   importacao     = importacao
								   )			
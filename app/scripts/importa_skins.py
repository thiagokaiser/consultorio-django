import csv
from app.models import LayoutSkin

print('1 - Exporta Skins')
print('2 - Importa Skins')
acao = input('Escolha uma opcao:')
if acao == '2':
	print('-- Eliminando Registros Skins --')
	skins = LayoutSkin.objects.all()
	for i in skins:
		print(i.descricao)
		i.delete()

	print('--------------------------------')
	print('---- Importando novas Skins ----')

	with open('app/scripts/skins.csv', encoding='utf-8') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';')

		for row in reader:		
			print(row['descricao'])
			LayoutSkin.objects.create(descricao=row['descricao'],
									  nome_css=row['nome_css'])

	print('--------------------------------')
if acao == '1':
	print('---- Exportando Registros ----')	

	with open('app/scripts/skins.csv', 'w', newline='') as csvfile:
		arquivo = csv.writer(csvfile, delimiter=';')
		
		arquivo.writerow(['descricao','nome_css'])

		skins = LayoutSkin.objects.all()
		for i in skins:	    
			print(i.descricao)
			arquivo.writerow([i.descricao,i.nome_css])
	    
	print('------------------------------')
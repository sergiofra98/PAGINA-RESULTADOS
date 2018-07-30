# # -*- coding: utf-8 -*-

from flask import Flask 
from flask import request
from functools import reduce

import json
import datetime
import locale

locale.setlocale( locale.LC_ALL, '' )
#locale.currency( row[1], grouping = True ) 
app = Flask(__name__)

@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
	return response

url_base='/MasNomina/MonitorCobranza'

@app.route(url_base)
def hello():
	return "Monitor Cobranza Estatus[OK]"

@app.route(url_base+'/general',methods=['GET']) 
def general():
	division = request.args.get('division')
	mes = request.args.get('mes')
	if division == None:
		print('No limita consulta por division')#define consulta para toda las divisiones
	if mes == None:
		print('Limita a mes actual')#define consulta para mes actual
	
	#se realiza la consulta
	lista_retorno = {}
	

	#START CARTERA
	lista_resultado_cartera = []
	lista_resultado_cartera_pct = []
	lista_resultado_cartera_vigente = []
	lista_resultado_cartera_icv = []

	lista_cartera=[
					['VIGENTE', 600628 , 714611 , 715812],
					['VENCIDA', 19957 , 15971 , 16440],
					['CASTIGO CONTABLE', 30407 , 32239 , 32878],
					['CASTIGO FISCAL', 66738 , 98988 , 101281]
			]

	#Obtenemos totales
	mes1 = 'ABR17'
	mes2 = 'MAR18'
	mes3 = 'ABR18'

	totales_cartera = ['TOTAL',0 ,0 ,0]

	lista_resultado_cartera.append(['NOMBRE', mes1, mes2, mes3])

	for i, row in enumerate(lista_cartera, 1):
		registro = []

		registro.append(row[0])
		registro.append('{:0,.2f}'.format(row[1]))
		registro.append('{:0,.2f}'.format(row[2]))
		registro.append('{:0,.2f}'.format(row[3]))

		totales_cartera[1] += row[1]
		totales_cartera[2] += row[2]
		totales_cartera[3] += row[3]
		lista_resultado_cartera.append(registro)

	lista_resultado_cartera_pct.append(['Nombre','ABR17', 'MAR18', 'ABR18', 'semaforo'])

	for i, row in enumerate(lista_cartera, 1):
		temp = []
		temp.append(row[0])
		temp.append('{:0,.2f}%'.format(100*(row[1]/totales_cartera[1])))
		temp.append('{:0,.2f}%'.format(100*(row[2]/totales_cartera[2])))
		temp.append('{:0,.2f}%'.format(100*(row[3]/totales_cartera[3])))
		if i == 1:
			if row[3]/totales_cartera[3] > row[2]/totales_cartera[2]:
				temp.append('verde')
			else:
				temp.append('rojo')
		else:
			if row[3]/totales_cartera[3] < row[2]/totales_cartera[2]:
				temp.append('verde')
			else:
				temp.append('rojo')
		lista_resultado_cartera_pct.append(temp)

	lista_resultado_cartera_vigente.append(lista_cartera[0][1] + lista_cartera[1][1])
	lista_resultado_cartera_vigente.append(lista_cartera[0][2] + lista_cartera[1][2])
	lista_resultado_cartera_vigente.append(lista_cartera[0][3] + lista_cartera[1][3])
	print(lista_resultado_cartera_vigente)

	lista_resultado_cartera_icv.append(['NOMBRE', mes1, mes2, mes3])

	aux_icv = []
	aux_icv.append('ICV' )
	aux_icv.append('{:0,.2f}%'.format(100*(lista_cartera[1][1] / lista_resultado_cartera_vigente[0])))
	aux_icv.append('{:0,.2f}%'.format(100*(lista_cartera[1][2] / lista_resultado_cartera_vigente[1])))
	aux_icv.append('{:0,.2f}%'.format(100*(lista_cartera[1][3] / lista_resultado_cartera_vigente[2])))
	lista_resultado_cartera_icv.append(aux_icv)

	aux_icv = []
	aux_icv.append('ICV Operativo' )
	aux_icv.append('{:0,.2f}%'.format(100*((lista_cartera[1][1] + lista_cartera[2][1] + lista_cartera[3][1])/totales_cartera[1])))
	aux_icv.append('{:0,.2f}%'.format(100*((lista_cartera[1][2] + lista_cartera[2][2] + lista_cartera[3][2])/totales_cartera[2])))
	aux_icv.append('{:0,.2f}%'.format(100*((lista_cartera[1][3] + lista_cartera[2][3] + lista_cartera[3][3])/totales_cartera[3])))
	lista_resultado_cartera_icv.append(aux_icv)

	aux_pcts = {}
	aux_pcts['ACA'] = '{:0,.2f}%'.format(100*((lista_resultado_cartera_vigente[2] / lista_resultado_cartera_vigente[0]) - 1))
	aux_pcts['MA'] = '{:0,.2f}%'.format(100*((lista_resultado_cartera_vigente[2] / lista_resultado_cartera_vigente[1]) - 1))

	
	totales_cartera[1] = '{:0,.2f}'.format(totales_cartera[1])
	totales_cartera[2] = '{:0,.2f}'.format(totales_cartera[2])
	totales_cartera[3] = '{:0,.2f}'.format(totales_cartera[3])
	lista_resultado_cartera.append(totales_cartera)

	lista_resultado_cartera_vigente[0] = '{:0,.2f}'.format(lista_resultado_cartera_vigente[0])
	lista_resultado_cartera_vigente[1] = '{:0,.2f}'.format(lista_resultado_cartera_vigente[1])
	lista_resultado_cartera_vigente[2] = '{:0,.2f}'.format(lista_resultado_cartera_vigente[2])

	lista_retorno['cartera_datos'] = lista_resultado_cartera
	lista_retorno['cartera_datos_pct'] = lista_resultado_cartera_pct
	lista_retorno['cartera_datos_vigente'] = lista_resultado_cartera_vigente
	lista_retorno['icv'] = lista_resultado_cartera_icv
	lista_retorno['pct_vs'] = aux_pcts
	#END CARTERA

	#START CARTERA POR BUCKETS
	lista_resultado_cartera = []
	lista_resultado_cartera_pct = []

	lista_cartera=[
					['0', 497986 , 598494 , 626969],
					['1-29', 58264 , 34279 , 40925],
					['30-59', 10912 , 56604 , 14171],
					['60-89', 33466 , 25234 , 33747],
					['90-119', 9312 , 3160 , 8231],
					['120-149', 3430 , 6552 , 2595],
					['150-179', 7215 , 6259 , 5614],
					['180-364', 30407 , 32239 , 32878],
					['365 o +', 66738 , 98988 , 101281]
			]

	#Obtenemos totales
	totales_cartera = ['TOTAL',0 ,0 ,0]
	totales_cartera[1] = 0
	totales_cartera[2] = 0
	totales_cartera[3]= 0

	lista_resultado_cartera.append([mes1, mes2, mes3])
	for i, row in enumerate(lista_cartera, 1):
		registro = []
		registro.append(row[0])
		registro.append('{:0,.2f}'.format(row[1]))
		registro.append('{:0,.2f}'.format(row[2]))
		registro.append('{:0,.2f}'.format(row[3]))

		totales_cartera[1] += row[1]
		totales_cartera[2] += row[2]
		totales_cartera[3]+= row[3]
		lista_resultado_cartera.append(registro)
	
	lista_resultado_cartera_pct.append([mes1, mes2, mes3, 'SEMAFORO'])

	for i, row in enumerate(lista_cartera, 1):
		registro = []

		registro.append(row[0])
		registro.append('{:0,.2f}%'.format(100*(row[1]/totales_cartera[1])))
		registro.append('{:0,.2f}%'.format(100*(row[2]/totales_cartera[2])))
		registro.append('{:0,.2f}%'.format(100*(row[3]/totales_cartera[3])))

		if i == 1:
			if row[3]/totales_cartera[3]> row[2]/totales_cartera[2]:
				registro.append('verde')
			else:
				registro.append('rojo')
		else:
			if row[3]/totales_cartera[3]< row[2]/totales_cartera[2]:
				registro.append('verde')
			else:
				registro.append('rojo')
		lista_resultado_cartera_pct.append(registro)

	totales_cartera[1] = '{:0,.2f}'.format(totales_cartera[1])
	totales_cartera[2] = '{:0,.2f}'.format(totales_cartera[2])
	totales_cartera[3]= '{:0,.2f}'.format(totales_cartera[3])
	lista_resultado_cartera.append(totales_cartera)

	lista_retorno['cartera_datos_bucket'] = lista_resultado_cartera
	lista_retorno['cartera_datos_pct_bucket'] = lista_resultado_cartera_pct
	#END CARTERA POR BUCKETS

	#START CARTERA OPERATIVA
	lista_resultado_cartera = []
	lista_resultado_cartera_totales = {}

	lista_cartera=[
					['100%', 601192 , 2916 , 7573 , 4748],
					['90-99%', 19751 , 153 , 613 , 115],
					['60-89%', 21494 , 1834 , 2148 , 1524],
					['30-59%', 6004 , 1705 , 2165 , 2271],
					['1-29%', 1819 , 1237 , 1984 , 4767],
					['POR INSTALAR', 44079 , 70 , 66 , 65],
					['CERO', 13886 , 3418 , 7054 , 15266],
					['BAJAS en recuperacion', 5283 , 3525 , 8540 , 56462],
					['BAJAS', 1321 , 881 , 2135 , 14115],
					['DEFUNCIONES', 982 , 583 , 567 , 1239],
					['FRAUDES', 0 , 120 , 32 , 710]
			]

	#Obtenemos totales
	totales_cartera = {}
	totales_cartera['nombre'] = 'TOTAL'
	totales_cartera['VIGENTE'] = 0
	totales_cartera['VENCIDA'] = 0
	totales_cartera['CASTIGO_CONTABLE'] = 0
	totales_cartera['CASTIGO_FISCAL'] = 0
	totales_cartera['TOTAL'] = 0


	for i, row in enumerate(lista_cartera, 1):
		registro = {}
		registro['id'] = i
		registro['nombre'] = row[0]
		registro['VIGENTE'] = '{:0,.2f}'.format(row[1])
		registro['VENCIDA'] = '{:0,.2f}'.format(row[2])
		registro['CASTIGO_CONTABLE'] = '{:0,.2f}'.format(row[3])
		registro['CASTIGO_FISCAL'] = '{:0,.2f}'.format(row[4])
		registro['TOTAL'] = '{:0,.2f}'.format(row[1] + row[2] + row[3] + row[4])
		
		totales_cartera['VIGENTE'] += row[1]
		totales_cartera['VENCIDA'] += row[2]
		totales_cartera['CASTIGO_CONTABLE'] += row[3]
		totales_cartera['CASTIGO_FISCAL'] += row[4]
		totales_cartera['TOTAL'] += (row[1] + row[2] + row[3] + row[4])
		
		lista_resultado_cartera.append(registro)

	totales_cartera['id'] = len(lista_resultado_cartera) + 1

	lista_resultado_cartera_totales['pcts'] = float(lista_resultado_cartera[0]['TOTAL'].replace(',','')) + float(lista_resultado_cartera[1]['TOTAL'].replace(',','')) + float(lista_resultado_cartera[2]['TOTAL'].replace(',','')) + float(lista_resultado_cartera[3]['TOTAL'].replace(',','')) + float(lista_resultado_cartera[4]['TOTAL'].replace(',',''))
	lista_resultado_cartera_totales['instalar'] = float(lista_resultado_cartera[5]['TOTAL'].replace(',',''))
	lista_resultado_cartera_totales['cero'] = float(lista_resultado_cartera[6]['TOTAL'].replace(',',''))
	lista_resultado_cartera_totales['bajas'] = float(lista_resultado_cartera[7]['TOTAL'].replace(',','')) + float(lista_resultado_cartera[8]['TOTAL'].replace(',',''))
	lista_resultado_cartera_totales['fraudes_defunciones'] = float(lista_resultado_cartera[9]['TOTAL'].replace(',','')) + float(lista_resultado_cartera[10]['TOTAL'].replace(',',''))
	
	lista_resultado_cartera_totales['pcts_pct'] = '{:0,.2f}%'.format((lista_resultado_cartera_totales['pcts']/totales_cartera['TOTAL'])*100)
	lista_resultado_cartera_totales['instalar_pct'] = '{:0,.2f}%'.format((lista_resultado_cartera_totales['instalar']/totales_cartera['TOTAL'])*100)
	lista_resultado_cartera_totales['cero_pct'] = '{:0,.2f}%'.format((lista_resultado_cartera_totales['cero']/totales_cartera['TOTAL'])*100)
	lista_resultado_cartera_totales['bajas_pct'] = '{:0,.2f}%'.format((lista_resultado_cartera_totales['bajas']/totales_cartera['TOTAL'])*100)
	lista_resultado_cartera_totales['fraudes_defunciones_pct'] = '{:0,.2f}%'.format((lista_resultado_cartera_totales['fraudes_defunciones']/totales_cartera['TOTAL'])*100)

	lista_resultado_cartera_totales['pcts'] = '{:0,.2f}'.format(lista_resultado_cartera_totales['pcts'])
	lista_resultado_cartera_totales['instalar'] = '{:0,.2f}'.format(lista_resultado_cartera_totales['instalar'])
	lista_resultado_cartera_totales['cero'] = '{:0,.2f}'.format(lista_resultado_cartera_totales['cero'])
	lista_resultado_cartera_totales['bajas'] = '{:0,.2f}'.format(lista_resultado_cartera_totales['bajas'])
	lista_resultado_cartera_totales['fraudes_defunciones'] = '{:0,.2f}'.format(lista_resultado_cartera_totales['fraudes_defunciones'])

	totales_cartera['VIGENTE'] = '{:0,.2f}'.format(totales_cartera['VIGENTE'])
	totales_cartera['VENCIDA'] = '{:0,.2f}'.format(totales_cartera['VENCIDA'])
	totales_cartera['CASTIGO_CONTABLE'] = '{:0,.2f}'.format(totales_cartera['CASTIGO_CONTABLE'])
	totales_cartera['CASTIGO_FISCAL'] = '{:0,.2f}'.format(totales_cartera['CASTIGO_FISCAL'])
	totales_cartera['TOTAL'] = '{:0,.2f}'.format(totales_cartera['TOTAL'])
	lista_resultado_cartera.append(totales_cartera)

	lista_retorno['cartera_datos_operativa'] = lista_resultado_cartera
	lista_retorno['cartera_datos_operativa_totales'] = lista_resultado_cartera_totales
	#END CARTERA OPERATIVA

	#START CARTERA OPERATIVA  X COBRAR
	lista_resultado_cartera = []
	lista_resultado_cartera_totales = {}

	#Obtenemos totales
	totales_cartera = {}
	totales_cartera['nombre'] = 'TOTAL'
	totales_cartera['VIGENTE'] = 0
	totales_cartera['VENCIDA'] = 0
	totales_cartera['CASTIGO_CONTABLE'] = 0
	totales_cartera['CASTIGO_FISCAL'] = 0
	totales_cartera['TOTAL'] = 0


	for i, row in enumerate(lista_cartera, 1):
		registro = {}
		registro['id'] = i
		registro['nombre'] = row[0]
		registro['VIGENTE'] = '{:0,.2f}'.format(row[1]*1.4)
		registro['VENCIDA'] = '{:0,.2f}'.format(row[2]*1.4)
		registro['CASTIGO_CONTABLE'] = '{:0,.2f}'.format(row[3]*1.4)
		registro['CASTIGO_FISCAL'] = '{:0,.2f}'.format(row[4]*1.4)
		registro['TOTAL'] = '{:0,.2f}'.format((row[1] + row[2] + row[3] + row[4])*1.4)
		
		totales_cartera['VIGENTE'] += row[1]*1.4
		totales_cartera['VENCIDA'] += row[2]*1.4
		totales_cartera['CASTIGO_CONTABLE'] += row[3]*1.4
		totales_cartera['CASTIGO_FISCAL'] += row[4]*1.4
		totales_cartera['TOTAL'] += ((row[1] + row[2] + row[3] + row[4])*1.4)
		
		lista_resultado_cartera.append(registro)

	totales_cartera['id'] = len(lista_resultado_cartera) + 1

	lista_resultado_cartera_totales['pcts'] = float(lista_resultado_cartera[0]['TOTAL'].replace(',','')) + float(lista_resultado_cartera[1]['TOTAL'].replace(',','')) + float(lista_resultado_cartera[2]['TOTAL'].replace(',','')) + float(lista_resultado_cartera[3]['TOTAL'].replace(',','')) + float(lista_resultado_cartera[4]['TOTAL'].replace(',',''))
	lista_resultado_cartera_totales['instalar'] = float(lista_resultado_cartera[5]['TOTAL'].replace(',',''))
	lista_resultado_cartera_totales['cero'] = float(lista_resultado_cartera[6]['TOTAL'].replace(',',''))
	lista_resultado_cartera_totales['bajas'] = float(lista_resultado_cartera[7]['TOTAL'].replace(',','')) + float(lista_resultado_cartera[8]['TOTAL'].replace(',',''))
	lista_resultado_cartera_totales['fraudes_defunciones'] = float(lista_resultado_cartera[9]['TOTAL'].replace(',','')) + float(lista_resultado_cartera[10]['TOTAL'].replace(',',''))
	
	lista_resultado_cartera_totales['pcts_pct'] = '{:0,.2f}%'.format((lista_resultado_cartera_totales['pcts']/totales_cartera['TOTAL'])*100)
	lista_resultado_cartera_totales['instalar_pct'] = '{:0,.2f}%'.format((lista_resultado_cartera_totales['instalar']/totales_cartera['TOTAL'])*100)
	lista_resultado_cartera_totales['cero_pct'] = '{:0,.2f}%'.format((lista_resultado_cartera_totales['cero']/totales_cartera['TOTAL'])*100)
	lista_resultado_cartera_totales['bajas_pct'] = '{:0,.2f}%'.format((lista_resultado_cartera_totales['bajas']/totales_cartera['TOTAL'])*100)
	lista_resultado_cartera_totales['fraudes_defunciones_pct'] = '{:0,.2f}%'.format((lista_resultado_cartera_totales['fraudes_defunciones']/totales_cartera['TOTAL'])*100)

	lista_resultado_cartera_totales['pcts'] = '{:0,.2f}'.format(lista_resultado_cartera_totales['pcts'])
	lista_resultado_cartera_totales['instalar'] = '{:0,.2f}'.format(lista_resultado_cartera_totales['instalar'])
	lista_resultado_cartera_totales['cero'] = '{:0,.2f}'.format(lista_resultado_cartera_totales['cero'])
	lista_resultado_cartera_totales['bajas'] = '{:0,.2f}'.format(lista_resultado_cartera_totales['bajas'])
	lista_resultado_cartera_totales['fraudes_defunciones'] = '{:0,.2f}'.format(lista_resultado_cartera_totales['fraudes_defunciones'])

	totales_cartera['VIGENTE'] = '{:0,.2f}'.format(totales_cartera['VIGENTE'])
	totales_cartera['VENCIDA'] = '{:0,.2f}'.format(totales_cartera['VENCIDA'])
	totales_cartera['CASTIGO_CONTABLE'] = '{:0,.2f}'.format(totales_cartera['CASTIGO_CONTABLE'])
	totales_cartera['CASTIGO_FISCAL'] = '{:0,.2f}'.format(totales_cartera['CASTIGO_FISCAL'])
	totales_cartera['TOTAL'] = '{:0,.2f}'.format(totales_cartera['TOTAL'])
	lista_resultado_cartera.append(totales_cartera)

	lista_retorno['cartera_datos_operativa_cobrar'] = lista_resultado_cartera
	lista_retorno['cartera_datos_operativa_totales_cobrar'] = lista_resultado_cartera_totales
	#END CARTERA OPERATIVA X COBRAR

	#START CARTERA NEVER PAID
	lista_resultado_cartera = []

	lista_cartera=[
					['0', 44632449 , 48882050 , 45728698],
					['1-29', 3720389 , 342088 , 590839],
					['30-59', 208177 , 2301836 , 226049],
					['60-89', 4423923 , 817035 , 1041132],
					['90-119', 1198200 , 382012 , 582725],
					['120-149', 219703 , 865198 , 346408],
					['150-179', 782058 , 1034091 , 716312],
					['180-364', 4148246 , 4091867 , 4912132],
					['365 o +', 9586286 , 12349604 , 11730876]
			]

	#Obtenemos totales
	totales_cartera = ['TOTAL',0 ,0 ,0]
	totales_cartera[1] = 0
	totales_cartera[2] = 0
	totales_cartera[3]= 0

	lista_resultado_cartera.append(['NOMBRE', mes1, mes2, mes3])
	for i, row in enumerate(lista_cartera, 1):
		registro = []
		registro.append(row[0])
		registro.append('{:0,.2f}'.format(row[1]))
		registro.append('{:0,.2f}'.format(row[2]))
		registro.append('{:0,.2f}'.format(row[3]))

		if not i == 1:
			totales_cartera[1] += row[1]
			totales_cartera[2] += row[2]
			totales_cartera[3]+= row[3]
		lista_resultado_cartera.append(registro)

	totales_cartera[1] = '{:0,.2f}'.format(totales_cartera[1])
	totales_cartera[2] = '{:0,.2f}'.format(totales_cartera[2])
	totales_cartera[3]= '{:0,.2f}'.format(totales_cartera[3])
	lista_resultado_cartera.append(totales_cartera)

	lista_retorno['cartera_datos_never_paid'] = lista_resultado_cartera
	#END CARTERA NEVER PAID

	#START CARTERA NEVER PAID CREDITOS
	lista_resultado_cartera = []

	lista_cartera=[
					['0', 1497 , 1456 ,1553 ],
					['1-29', 61 , 15 ,29 ],
					['30-59', 14 , 60 ,10 ],
					['60-89', 176 , 45 ,42 ],
					['90-119', 48 , 22 ,33 ],
					['120-149', 9 , 46 ,20 ],
					['150-179', 32 , 45 ,44 ],
					['180-364', 129 , 198 ,236 ],
					['365 o +', 437 , 551 ,543 ]
			]

	#Obtenemos totales
	totales_cartera = []
	totales_cartera.append('TOTAL')
	totales_cartera.append(0)
	totales_cartera.append(0)
	totales_cartera.append(0)

	lista_resultado_cartera.append(['NOMBRE', mes1, mes2, mes3])

	for i, row in enumerate(lista_cartera, 1):
		registro = []

		registro.append(row[0])
		registro.append('{:0,.2f}'.format(row[1]))
		registro.append('{:0,.2f}'.format(row[2]))
		registro.append('{:0,.2f}'.format(row[3]))

		if not i == 1:
			totales_cartera[1] += row[1]
			totales_cartera[2] += row[2]
			totales_cartera[3]+= row[3]
		lista_resultado_cartera.append(registro)

	totales_cartera[1] = '{:0,.2f}'.format(totales_cartera[1])
	totales_cartera[2] = '{:0,.2f}'.format(totales_cartera[2])
	totales_cartera[3]= '{:0,.2f}'.format(totales_cartera[3])
	lista_resultado_cartera.append(totales_cartera)

	lista_retorno['cartera_datos_never_paid_creditos'] = lista_resultado_cartera
	#END CARTERA NEVER PAID CREDITOS

	return json.dumps(lista_retorno)


@app.route(url_base+'/inactividad_atraso',methods=['GET']) 
def inactividad_atraso():
	division = request.args.get('division')
	mes = request.args.get('mes')
	if division == None:
		print('No limita consulta por division')#define consulta para toda las divisiones
	if mes == None:
		print('Limita a mes actual')#define consulta para mes actual
	
	#se realiza la consulta
	lista_resultado = []
	lista_resultado_pct = []
	lista_datos=[['Nunca Instalados,', 446067883 , 20616801 , 4862620 , 2721655 , 2721655 , 2721655 , 2721655 , 1800754 , 2013615 , 1672655 , 27702112 ],
				['Con Descuento,', 290328852 , 224716555 , 45696120 , 14874650 , 8459094 , 8091618 , 5613789 , 4208939 , 2908685 , 2110689 , 14185385 ],
				['Sin pago 30', 27729957 , 16501716 , 10730680 , 4074488 , 1974146 , 1483467 , 1773000 , 1379130 , 1113131 , 786985 , 4627596], 
				['Sin pago 60', 950778 , 3539560 , 2778711 , 2271862 , 1068169 , 650073 , 820780 , 744019 , 762807 , 537772 , 2381762], 
				['Sin pago 90', 0   , 255609 , 813249 , 1358210 , 947973 , 570390 , 307464 , 625086 , 1085309 , 720427 , 3464533], 
				['Sin pago 120', 0   , 0   , 186812 , 1114879 , 889479 , 949256 , 460416 , 119146 , 101029 , 184724 , 1144365], 
				['Sin pago 150', 0   , 0   , 15517 , 245966 , 809675 , 558336 , 1108994 , 328716 , 186671 , 87886 , 1169324], 
				['Sin pago 180', 0   , 0   , 0   , 0   , 202650 , 826487 , 441344 , 868548 , 420742 , 365953 , 2485747], 
				['Sin pago 210', 0   , 0   , 0   , 0   , 476 , 271508 , 743983 , 794660 , 1202797 , 150686 , 1673698], 
				['Sin pago 240', 0   , 0   , 0   , 0   , 0   , 0   , 190613 , 556269 , 601964 , 874866 , 2286251], 
				['Sin pago 270', 0   , 0   , 0   , 0   , 0   , 0   , 0   , 293660 , 750879 , 1048404 , 2405571], 
				['Sin pago 300', 0   , 0   , 0   , 0   , 0   , 0   , 0   , 0   , 234687 , 1254672 , 140267048 ]
			]

	#Obtenemos totales
	totales = {}
	totales['nombre'] = 'TOTAL'
	totales['actual'] = 0
	totales['atraso_30'] = 0
	totales['atraso_60'] = 0
	totales['atraso_90'] = 0
	totales['atraso_120'] = 0
	totales['atraso_150'] = 0
	totales['atraso_180'] = 0
	totales['atraso_210'] = 0
	totales['atraso_240'] = 0
	totales['atraso_270'] = 0
	totales['atraso_mas_270'] = 0
	totales['total'] = 0

	for i, row in enumerate(lista_datos, 1):
		registro = {}
		registro['id'] = i
		registro['nombre'] = row[0]
		registro['actual'] = '{:0,.2f}'.format(row[1])
		registro['atraso_30'] = '{:0,.2f}'.format(row[2])
		registro['atraso_60'] = '{:0,.2f}'.format(row[3])
		registro['atraso_90'] = '{:0,.2f}'.format(row[4])
		registro['atraso_120'] = '{:0,.2f}'.format(row[5])
		registro['atraso_150'] = '{:0,.2f}'.format(row[6])
		registro['atraso_180'] = '{:0,.2f}'.format(row[7])
		registro['atraso_210'] = '{:0,.2f}'.format(row[8])
		registro['atraso_240'] = '{:0,.2f}'.format(row[9])
		registro['atraso_270'] = '{:0,.2f}'.format(row[10])
		registro['atraso_mas_270'] = '{:0,.2f}'.format(row[11])
		totales['actual'] += row[1]
		totales['atraso_30'] += row[2]
		totales['atraso_60'] += row[3]
		totales['atraso_90'] += row[4]
		totales['atraso_120'] += row[5]
		totales['atraso_150'] += row[6]
		totales['atraso_180'] += row[7]
		totales['atraso_210'] += row[8]
		totales['atraso_240'] += row[9]
		totales['atraso_270'] += row[10]
		totales['atraso_mas_270'] += row[11]
		aux_total = 0
		for j, row2 in enumerate(row):
			if not j == 0:
				aux_total += row2
		registro['total'] = '{:0,.2f}'.format(aux_total)
		totales['total'] += aux_total
		lista_resultado.append(registro)
	

	totales_pct = {}
	totales_pct['nombre'] = 'TOTAL'
	totales_pct['actual'] = 0
	totales_pct['atraso_30'] = 0
	totales_pct['atraso_60'] = 0
	totales_pct['atraso_90'] = 0
	totales_pct['atraso_120'] = 0
	totales_pct['atraso_150'] = 0
	totales_pct['atraso_180'] = 0
	totales_pct['atraso_210'] = 0
	totales_pct['atraso_240'] = 0
	totales_pct['atraso_270'] = 0
	totales_pct['atraso_mas_270'] = 0
	for i, row in enumerate(lista_datos, 1):
		registro = {}
		registro['id'] = i
		registro['nombre'] = row[0]
		registro['actual'] = '{:0,.2f}%'.format((row[1]/totales['total'])*100)
		registro['atraso_30'] = '{:0,.2f}%'.format((row[2]/totales['total'])*100)
		registro['atraso_60'] = '{:0,.2f}%'.format((row[3]/totales['total'])*100)
		registro['atraso_90'] = '{:0,.2f}%'.format((row[4]/totales['total'])*100)
		registro['atraso_120'] = '{:0,.2f}%'.format((row[5]/totales['total'])*100)
		registro['atraso_150'] = '{:0,.2f}%'.format((row[6]/totales['total'])*100)
		registro['atraso_180'] = '{:0,.2f}%'.format((row[7]/totales['total'])*100)
		registro['atraso_210'] = '{:0,.2f}%'.format((row[8]/totales['total'])*100)
		registro['atraso_240'] = '{:0,.2f}%'.format((row[9]/totales['total'])*100)
		registro['atraso_270'] = '{:0,.2f}%'.format((row[10]/totales['total'])*100)
		registro['atraso_mas_270'] = '{:0,.2f}%'.format((row[11]/totales['total'])*100)
		totales_pct['actual'] += (row[1]/totales['total'])
		totales_pct['atraso_30'] += (row[2]/totales['total'])
		totales_pct['atraso_60'] += (row[3]/totales['total'])
		totales_pct['atraso_90'] += (row[4]/totales['total'])
		totales_pct['atraso_120'] += (row[5]/totales['total'])
		totales_pct['atraso_150'] += (row[6]/totales['total'])
		totales_pct['atraso_180'] += (row[7]/totales['total'])
		totales_pct['atraso_210'] += (row[8]/totales['total'])
		totales_pct['atraso_240'] += (row[9]/totales['total'])
		totales_pct['atraso_270'] += (row[10]/totales['total'])
		totales_pct['atraso_mas_270'] += (row[11]/totales['total'])
		lista_resultado_pct.append(registro)

	totales['id'] = len(lista_resultado) + 1
	totales['actual'] = '{:0,.2f}'.format(totales['actual'])
	totales['atraso_30'] = '{:0,.2f}'.format(totales['atraso_30'])
	totales['atraso_60'] = '{:0,.2f}'.format(totales['atraso_60'])
	totales['atraso_90'] = '{:0,.2f}'.format(totales['atraso_90'])
	totales['atraso_120'] = '{:0,.2f}'.format(totales['atraso_120'])
	totales['atraso_150'] = '{:0,.2f}'.format(totales['atraso_150'])
	totales['atraso_180'] = '{:0,.2f}'.format(totales['atraso_180'])
	totales['atraso_210'] = '{:0,.2f}'.format(totales['atraso_210'])
	totales['atraso_240'] = '{:0,.2f}'.format(totales['atraso_240'])
	totales['atraso_270'] = '{:0,.2f}'.format(totales['atraso_270'])
	totales['atraso_mas_270'] = '{:0,.2f}'.format(totales['atraso_mas_270'])
	totales['total'] = '{:0,.2f}'.format(totales['total'])

	totales_pct['id'] = len(lista_resultado_pct) + 1
	totales_pct['actual'] = '{:0,.2f}%'.format((totales_pct['actual'])*100)
	totales_pct['atraso_30'] = '{:0,.2f}%'.format((totales_pct['atraso_30'])*100)
	totales_pct['atraso_60'] = '{:0,.2f}%'.format((totales_pct['atraso_60'])*100)
	totales_pct['atraso_90'] = '{:0,.2f}%'.format((totales_pct['atraso_90'])*100)
	totales_pct['atraso_120'] = '{:0,.2f}%'.format((totales_pct['atraso_120'])*100)
	totales_pct['atraso_150'] = '{:0,.2f}%'.format((totales_pct['atraso_150'])*100)
	totales_pct['atraso_180'] = '{:0,.2f}%'.format((totales_pct['atraso_180'])*100)
	totales_pct['atraso_210'] = '{:0,.2f}%'.format((totales_pct['atraso_210'])*100)
	totales_pct['atraso_240'] = '{:0,.2f}%'.format((totales_pct['atraso_240'])*100)
	totales_pct['atraso_270'] = '{:0,.2f}%'.format((totales_pct['atraso_270'])*100)
	totales_pct['atraso_mas_270'] = '{:0,.2f}%'.format((totales_pct['atraso_mas_270'])*100)
	
	lista_resultado.append(totales)
	lista_resultado_pct.append(totales_pct)

	lista_retorno = {}
	lista_retorno['datos'] = lista_resultado
	lista_retorno['porcentajes'] = lista_resultado_pct

	return json.dumps(lista_retorno)


if __name__ == '__main__':	
	#si Rest.py
	app.run(host="127.0.0.1",debug=True, port=9999, threaded=True)
















    
	


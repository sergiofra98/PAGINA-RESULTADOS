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

url_base='/MasNomina/MonitorVentas'

@app.route(url_base)
def hello():
	return "Monitor Ventas Estatus[OK]"

#combo box de divisiones
@app.route(url_base+'/consulta_divisiones',methods=['GET']) 
def consulta_divisiones():
	lista_divisiones = []
	division={}
	division['id_div'] = 1
	division['nombre'] = 'CENTRO'
	lista_divisiones.append(division)
	division={}
	division['id_div'] = 2
	division['nombre'] = 'SUR'
	lista_divisiones.append(division)
	division={}
	division['id_div'] = 3
	division['nombre'] = 'NORESTE'
	lista_divisiones.append(division)
	division={}
	division['id_div'] = 4
	division['nombre'] = 'NORTE'
	lista_divisiones.append(division)
	division={}
	division['id_div'] = 5
	division['nombre'] = 'VM NORTE'
	lista_divisiones.append(division)
	division={}
	division['id_div'] = 6
	division['nombre'] = 'VM SUR'
	lista_divisiones.append(division)
	division={}
	division['id_div'] = 7
	division['nombre'] = 'VM CENTRO'
	lista_divisiones.append(division)
	return json.dumps(lista_divisiones)
	
#combo box de periodos
@app.route(url_base+'/consulta_periodos',methods=['GET']) 
def consulta_periodos():
	lista_periodos = []
	num_periodos = 18
	today = datetime.datetime.today()
	mes = 0
	anio = 0
	mes = int(today.strftime("%m"))
	anio = int(today.strftime("%Y"))
	periodo = 0
	while periodo < num_periodos:
		if periodo > 0:					
			if mes == 1:
				anio = anio -1
				mes = 12
			else:
				mes = mes - 1
		if len(str(mes)) == 1:			
			id_periodo = str(anio) + '0' + str(mes)	
		else:
			id_periodo = str(anio) + str(mes)	
		periodo += 1
		data_periodo = {}
		data_periodo['id_per'] = id_periodo
		data_periodo['per'] = id_periodo
		lista_periodos.append(data_periodo)
	return json.dumps(lista_periodos)
	

#tabla x convenio colocacion
@app.route(url_base+'/consulta_convenio_colocacion',methods=['GET']) 
def consulta_convenio_colocacion():
	division = request.args.get('division')
	mes = request.args.get('mes')
	if division == None:
		print('No limita consulta por division')#define consulta para toda las divisiones
	if mes == None:
		print('Limita a mes actual')#define consulta para mes actual
	
	#se realiza la consulta
	lista_resultado = []
	lista_datos=[['GOBIERNO DE HIDALGO',967203.15,379404.20,3707870.52],
				 ['SNTE 14 FEDERAL GUERRERO',332979,42000,1290814],
				 ['PEMEX',301332,0,988869],
				 ['SAGARPA',207681,0,739000],
				 ['INE',154272,343852,657500],
				 ['SENTE 23 FEDERAL PUEBLA',63500,0,189963],
				 ['IMSS PENSIONADOS',68055,107720,562569],
				 ['IMSS JUBILADOS',51853,272508,157500],
				 ['IMSS ACTIVOS',0,0,125762],
				 ['IMSS PARITARIA',0,15000,21000],
				 ['COBAEH',0,0,141980],
				 ['TELECOMM',0,0,3000]
				]

	#Obtenemos totales
	total_mes = 0
	total_mes_aa = 0
	total_acu = 0
	for row in lista_datos:
		total_mes = total_mes + row[1]
		total_mes_aa = total_mes_aa + row[2]
		total_acu = total_acu + row[3]
	
	contador = 1
	for row in lista_datos:
		registro = {}
		registro['id'] = contador
		registro['nombre'] = row[0]
		
		registro['total_mes'] = '{:0,.0f}'.format(row[1]) 
		total_mes_pct = (row[1] / total_mes) * 100.00
		registro['total_mes_pct'] = '{:0,.2f}%'.format(total_mes_pct) 
		
		registro['total_mes_aa'] = '{:0,.0f}'.format(row[2]) 
		total_mes_aa_pct = (row[2] / total_mes_aa) * 100.00
		registro['total_mes_aa_pct'] = '{:0,.2f}%'.format(total_mes_aa_pct)
		
		registro['total_acu'] = '{:0,.0f}'.format(row[3]) 
		total_acu_pct = (row[3] / total_acu) * 100.00
		registro['total_acu_pct'] = '{:0,.2f}%'.format(total_acu_pct)
		
		contador = contador + 1
		lista_resultado.append(registro)
	
	registro_totales = {}
	registro_totales['id'] = contador
	registro_totales['nombre'] = 'TOTAL'
	registro_totales['total_mes'] = '{:0,.0f}'.format(total_mes)
	registro_totales['total_mes_pct'] = '{:0,.2f}%'.format(100) 
	registro_totales['total_mes_aa'] = '{:0,.0f}'.format(total_mes_aa)
	registro_totales['total_mes_aa_pct'] = '{:0,.2f}%'.format(100) 
	registro_totales['total_acu'] = '{:0,.0f}'.format(total_acu)
	registro_totales['total_acu_pct'] = '{:0,.2f}%'.format(100) 
	
	lista_resultado.append(registro_totales)
	
	return json.dumps(lista_resultado)	
	
	
#tabla x convenio cartera
@app.route(url_base+'/consulta_convenio_cartera',methods=['GET']) 
def consulta_convenio_cartera():
	division = request.args.get('division')
	mes = request.args.get('mes')
	if division == None:
		print('No limita consulta por division')#define consulta para toda las divisiones
	if mes == None:
		print('Limita a mes actual')#define consulta para mes actual
	
	#se realiza la consulta
	lista_resultado = []
	#[nombres, mes actual, mes anterior, mes año anterior]
	lista_datos=[['GOBIERNO DE HIDALGO',4800,3500,2500],
				 ['SNTE 14 FEDERAL GUERRERO',45000,42000,30000],
				 ['PEMEX',23000,18000,15000],
				 ['SAGARPA',2000,1000,500],
				 ['INE',2000,1000,500],
				 ['SENTE 23 FEDERAL PUEBLA',2000,1000,500],
				 ['IMSS PENSIONADOS',2000,1000,500],
				 ['IMSS JUBILADOS',2000,1000,500],
				 ['IMSS ACTIVOS',2000,1000,500],
				 ['IMSS PARITARIA',0,0,500],
				 ['COBAEH',0,0,0],
				 ['TELECOMM',0,0,0]
				]
	
	
	#Obtenemos totales
	total_mes = 0
	total_ma = 0
	total_maa = 0
	#de esto podriamos hacer una consulta a DB con un SUM para quitarle carga al back
	#ya que si es mucha informacion la que se va a sacar entonces esta iteracion lo hara
	#más lento
	for row in lista_datos:
		total_mes += row[1]
		total_ma += row[2]
		total_maa += row[3]
	
	for i, row in enumerate(lista_datos):

		registro = {}
		registro['id'] = i+1
		registro['nombre'] = row[0]
		
		registro['total_mes'] = '{:0,.2f}'.format(row[1])
		registro['total_ma'] = '{:0,.2f}'.format(row[2])
		registro['total_maa'] = '{:0,.2f}'.format(row[3])
		
		registro['total_mes_vs_ma'] = '{:0,.2f}'.format(row[1]-row[2]) 
		registro['total_mes_vs_maa'] = '{:0,.2f}'.format(row[1]-row[3]) 

		if row[2] == 0:
			registro['total_mes_vs_ma_pct'] = '0.00%'
		else:
			pct_m_ma = 0
			pct_m_ma = (row[1] * 1.00)/ (row[2] * 1.00) - 1
			pct_m_ma = pct_m_ma * 100.00
			registro['total_mes_vs_ma_pct'] = '{:0,.2f}%'.format(pct_m_ma) 

			if pct_m_ma < 0:
				registro['colorMA'] = "rojo"
			else:
				registro['colorMA'] = "blanco"
		if row[3] == 0:
			registro['total_mes_vs_maa_pct'] = '0.00%'
		else:
			pct_m_maa = 0
			pct_m_maa = (row[1] * 1.00)/ (row[3] * 1.00) - 1
			pct_m_maa = pct_m_maa * 100.00
			registro['total_mes_vs_maa_pct'] = '{:0,.2f}%'.format(pct_m_maa)

			if pct_m_maa < 0:
				registro['colorMAA'] = "rojo"
			else:
				registro['colorMAA'] = "blanco"
	
		lista_resultado.append(registro)
	
	registro_totales = {}
	registro_totales['id'] = len(lista_resultado) + 1
	registro_totales['nombre'] = 'TOTAL'

	registro_totales['total_mes'] = '{:0,.2f}'.format(total_mes)
	registro_totales['total_ma'] = '{:0,.2f}'.format(total_ma)
	registro_totales['total_maa'] = '{:0,.2f}'.format(total_maa)

	registro_totales['total_mes_vs_ma'] = '{:0,.2f}'.format(total_mes-total_ma) 
	registro_totales['total_mes_vs_maa'] = '{:0,.2f}'.format(total_mes-total_maa)


	if total_ma == 0:
		registro_totales['total_mes_vs_ma_pct'] = '0.00%'
	else:
		registro_totales['total_mes_vs_ma_pct'] = '{:0,.2f}%'.format(((total_mes * 1.00) / (total_ma * 1.00)-1)*100) 
		polaridad = ((total_mes * 1.00) / (total_ma * 1.00)-1)*100
		if polaridad < 0:
			registro_totales['colorMA'] = "rojo"
		else:
			registro_totales['colorMA'] = "blanco"
	if total_maa == 0:
		registro_totales['total_mes_vs_maa_pct'] = '0.00%'
	else:
		polaridad = ((total_mes * 1.00)/ (total_maa * 1.00)-1)*100
		registro_totales['total_mes_vs_maa_pct'] = '{:0,.2f}%'.format(((total_mes * 1.00)/ (total_maa * 1.00)-1)*100)
		if polaridad < 0:
			registro_totales['colorMAA'] = "rojo"
		else:
			registro_totales['colorMAA'] = "blanco"
	
	lista_resultado.append(registro_totales)

	return json.dumps(lista_resultado)
	

#tabla venta x estado
@app.route(url_base+'/consulta_estado_colocacion',methods=['GET']) 
def consulta_estado_colocacion():
	division = request.args.get('division')
	"""
	divs=['centro','sur','norte','noreste','vm_norte','vm_sur','vm_centro']
	if div in divs:
		print (div)#consulta por la division
	else:
		return 'Division no encontrada'
	"""
	meses=['ENE-17','FEB-17','MAR-17','ABR-17','MAY-17','JUN-17','JUL-17','AGO-17','SEP-17','OCT-17','NOV-17','DIC-17','ENE-18','FEB-18','MAR-18','ABR-18']
	#[nombres, meses]
	lista_estados_todos=[
				['HIDALGO',38128,15654,180712,381427,399516,381346,423030,404383,490677,308609,245726,175715,876173,1318727,1079677,883818],
				['PUEBLA',121297,31021,55242,221927,227049,69000,173043,313290,115000,229127,292404,124423,289156,447978,557991,371353],
				['GUERRERO',0,25000,305000,177000,234734,456867,435856,299568,557175,504930,309023,142262,338514,315634,407835,372686],
				['GUANAJUATO',163649,33302,160201,109121,114192,168942,70432,87027,210791,164855,111408,213427,279147,110599,389762,183667],
				['QUERETARO',239233,195000,480982,156419,184994,87373,143277,20000,0,0,0,0,0,14110,3000,21000]
				]
	lista_estados_anio_actual=[
				['HIDALGO',876173,1318727,1079677,883818],
				['PUEBLA',289156,447978,557991,371353],
				['GUERRERO',338514,315634,407835,372686],
				['GUANAJUATO',279147,110599,389762,183667],
				['QUERETARO',0,14110,3000,21000]
				]
	lista_brokers_todos=[ 
					['BROKER_LEON',25173,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					['BROKER_PACHUCA_4',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,17000],
					['BROKER_PACHUCA_5',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,205000],
					['BROKER_PACHUCA_6',0,0,0,0,0,0,0,0,0,0,0,0,0,0,11000,82000],
					['BROKERGUERRERO',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10000]
				]
	lista_brokers_anio_actual=[ 
					['BROKER_LEON',0,0,0,0],
					['BROKER_PACHUCA_4',0,0,0,17000],
					['BROKER_PACHUCA_5',0,0,0,205000],
					['BROKER_PACHUCA_6',0,0,11000,82000],
					['BROKERGUERRERO',0,0,0,10000]
				]
	lista_asesores_todos=[ 
					['GUANAJUATO',4,3,4,3,3,3,3,3,3,3,4,3,3,3,3,4],
					['GUERRERO',2,6,4,7,2,2,2,8,8,8,7,7,10,9,9,14],
					['HIDALGO',4,4,4,4,3,3,3,3,5,3,4,4,5,4,4,5],
					['PUEBLA',7,6,7,6,3,2,1,5,1,6,6,6,4,4,5,5],
					['QUERETARO',4,2,2,2,5,5,3,3,4,3,0,0,3,4,3,3]
				]
	
	#Obtenemos totales
	total_mes_general = []
	total_mes_asesores = []
	total_mes_promedio = []
	#de esto podriamos hacer una consulta a DB con un SUM para quitarle carga al back
	#ya que si es mucha informacion la que se va a sacar entonces esta iteracion lo hara
	#más lento

	#calculos para sacar info estados
	lista_estados = calculo_x_estado(lista_estados_todos, lista_estados_anio_actual)
	#calculos para sacar info brokers
	lista_brokers = calculo_x_estado(lista_brokers_todos, lista_brokers_anio_actual)

	#calculos para sacar info total general
	total_general = {}
	total_general['nombre'] = 'Total General'
	total_general['valores'] = {}
	aux_estados = lista_estados[len(lista_estados)-1]
	aux_brokers = lista_brokers[len(lista_brokers)-1]
	for i, row in enumerate(lista_estados_todos[0], 1):
		if i == len(lista_estados_todos[0]):
			break
		else:
			total_general['valores'][str(i)] = '{:0,.2f}'.format(float(aux_estados['valores'][str(i)].replace(',','')) + float(aux_brokers['valores'][str(i)].replace(',','')))
	total_general['suma_anio'] = float(aux_estados['suma_anio'].replace(',','')) + float(aux_brokers['suma_anio'].replace(',',''))
	total_general['promedio_anio'] = '{:0,.2f}'.format(total_general['suma_anio']/2)
	total_general['suma_anio'] = '{:0,.2f}'.format(total_general['suma_anio'])

	#calculos para sacar info asesores
	lista_asesores = []
	total_asesores = {}
	total_asesores['nombre'] = 'TOTAL'
	total_asesores['valores'] = {}
	for i, row in enumerate(lista_asesores_todos, 1):
		registro = {}
		registro['id'] = i
		registro['nombre'] = row[0]
		registro['valores'] = {}
		for j, row2 in enumerate(row, 1):
			if j == len(row):
				break
			else:
				registro['valores'][str(j)] = row[j]
				total_asesores['valores'][str(j)] = total_asesores['valores'].get(str(j), 0) +row[j]

		lista_asesores.append(registro)
	lista_asesores.append(total_asesores)

	#calculos para sacar info promedios
	lista_promedio = []
	total_promedio = {}
	total_promedio['nombre'] = 'Total General'
	total_promedio['valores'] = {}
	for i, row in enumerate(lista_estados_todos, 1):
		registro = {}
		registro['id'] = i
		registro['nombre'] = row[0]
		registro['valores'] = []
		for j, row2 in enumerate(row, 1):
			temp = []
			if j == len(row):
				break
			else:
				if lista_asesores[i]['valores'][str(j)] == 0:
					temp.append(0)
				else:
					temp.append(float(lista_estados[i]['valores'][str(j)].replace(',','')) / float(lista_asesores[i]['valores'][str(j)]))

				if temp[0] >= 80001 and temp[0] <= 120000:
					temp.append('promedio')
				elif temp[0] > 120000:
					temp.append('bueno')
				else:
					temp.append('malo')

				temp[0] = '{:0,.2f}'.format(temp[0])

			registro['valores'].append(temp)

		lista_promedio.append(registro)

	total = []
	for i, row in enumerate(lista_estados_todos[0], 1):
		temp = []

		if i == len(lista_estados_todos[0]):
			break
		else:
			if lista_asesores[len(lista_asesores)-1]['valores'][str(i)] == 0:
				temp.append(0)
			else:
				temp.append(float(total_general['valores'][str(i)].replace(',','')) / lista_asesores[len(lista_asesores)-1]['valores'][str(i)])

			if temp[0] >= 80001 and temp[0] <= 120000:
				temp.append('promedio')
			elif temp[0] > 120000:
				temp.append('bueno')
			else:
				temp.append('malo')

			temp[0] = '{:0,.2f}'.format(temp[0])
		total.append(temp)

	total_promedio['id']=len(lista_promedio)+1
	total_promedio['valores']= total
	lista_promedio.append(total_promedio)

	retorno = {}
	retorno['estados'] = lista_estados
	retorno['brokers'] = lista_brokers
	retorno['promedios'] = lista_promedio
	retorno['asesores'] = lista_asesores
	retorno['total_general'] = total_general
	retorno['meses'] = meses

	return json.dumps(retorno)
	
def calculo_x_estado(lista_todo, lista_actual):
	lista_resultado = []
	total = {}
	total['nombre'] = 'TOTAL'
	total['valores'] = {}
	suma_anio_total = 0
	for i, row in enumerate(lista_todo, 1):
		registro = {}
		registro['id'] = i
		registro['nombre'] = row[0]
		registro['valores'] = {}
		for j, row2 in enumerate(row, 1):
			if j == len(row):
				break
			else:
				registro['valores'][str(j)] = '{:0,.2f}'.format(row[j])
				total['valores'][str(j)] = '{:0,.2f}'.format( float( total['valores'].get(str(j), '0').replace(',','') ) + row[j] )
		suma_anio = 0
		turno = lista_actual[i-1]
		for j, row2 in enumerate(turno, 1):
			if j == len(turno):
				break
			else:
				suma_anio += turno[j]
				suma_anio_total += turno[j]
		registro['suma_anio'] = '{:0,.2f}'.format(suma_anio)
		registro['promedio_anio'] = '{:0,.2f}'.format(suma_anio/(len(turno)-1))

		lista_resultado.append(registro)

	total['id'] = len(lista_resultado) + 1
	total['suma_anio'] = '{:0,.2f}'.format(suma_anio_total)
	total['promedio_anio'] = '{:0,.2f}'.format(suma_anio_total/len(lista_resultado))

	lista_resultado.append(total)
	
	return lista_resultado


# tabla costos x colocacion
@app.route(url_base+'/costos_colocacion',methods=['GET']) 
def costos_colocacion():
	division = request.args.get('division')
	mes = request.args.get('mes')
	if division == None:
		print('No limita consulta por division')#define consulta para toda las divisiones
	if mes == None:
		print('Limita a mes actual')#define consulta para mes actual
	
	#se realiza la consulta
	lista_resultado_mes = []
	lista_resultado_acumulado = []
	lista_resultado_costo = []
	lista_mes=[['Colocación', 2146525 ],
				['Comisiones', 146587 ],
				['Sueldos fijo', 201300 ],
				['Carga social + aguinaldo', 135202 ],
				['Viáticos', 9328 ],
				['Gasolina', 3746 ],
				['Costo autos', 16785 ],
				['Rentas', 11841 ]
			]
	
	lista_acumulado=[	['Colocación', 8654566],
						['Comisiones', 903101],
						['Sueldos fijo', 737250],
						['Carga social + aguinaldo', 433258],
						['Viáticos', 53263],
						['Gasolina', 14011],
						['Costo autos', 62058],
						['Rentas', 61527]
				]

	lista_costo=[	['ENE-18', '32.93%'],
					['FEB-18', '26.97%'],
					['MAR-18', '22.00%'],
					['ABR-18', '24.45%'],
					['MAY-18', '0.00%'],
					['JUN-18', '0.00%'],
					['JUL-18', '0.00%'],
					['AGO-18', '0.00%'],
					['SEP-18', '0.00%'],
					['OCT-18', '0.00%'],
					['NOV-18', '0.00%'],
					['DIC-18', '0.00%'],
					['TOTAL', '26.17%']
				]

	#Obtenemos totales
	total_mes = 0
	total_acumulado = 0
	for i, row in enumerate(lista_mes):
		if not i == 0:
			total_mes += row[1]
	for i, row in enumerate(lista_acumulado):
		if not i == 0:
			total_acumulado += row[1]

	for i, row in enumerate(lista_mes):
		registro = {}
		registro['id'] = i
		registro['nombre'] = row[0]
		registro['valor'] = '{:0,.2f}'.format(row[1])
		if i == 0:
			registro['porcentaje'] = '%'
		else:
			registro['porcentaje'] = '{:0,.2f}%'.format(((row[1] * 1.00) / total_mes) * 100.00)
		lista_resultado_mes.append(registro)

	for i, row in enumerate(lista_acumulado):
		registro = {}
		registro['id'] = i
		registro['nombre'] = row[0]
		registro['valor'] = '{:0,.2f}'.format(row[1])
		if i == 0:
			registro['porcentaje'] = '%'
		else:
			registro['porcentaje'] = '{:0,.2f}%'.format(((row[1] * 1.00)/ total_acumulado) * 100.00)
		lista_resultado_acumulado.append(registro)
	
	for i, row in enumerate(lista_costo):
		registro = {}
		registro['id'] = i
		registro['nombre'] = row[0]
		registro['porcentaje'] = row[1]
		lista_resultado_costo.append(registro)
	
	registro_totales = {}
	registro_totales['id'] = len(lista_mes) + 1
	registro_totales['nombre'] = 'TOTAL'
	registro_totales['valor'] = '{:0,.2f}'.format(total_mes)
	registro_totales['porcentaje'] = '100%'
	lista_resultado_mes.append(registro_totales)

	registro_totales = {}
	registro_totales['id'] = len(lista_acumulado) + 1
	registro_totales['nombre'] = 'TOTAL'
	registro_totales['valor'] = '{:0,.2f}'.format(total_acumulado)
	registro_totales['porcentaje'] = '100%'
	lista_resultado_acumulado.append(registro_totales)
	
	lista_resultado = {}
	lista_resultado['mes'] = lista_resultado_mes
	lista_resultado['acumulado'] = lista_resultado_acumulado
	lista_resultado['costo'] = lista_resultado_costo

	return json.dumps(lista_resultado)	
	

"""


#tabla plantilla
@app.route(url_base+'/vendedores',methods=['GET']) 
def vendedores():
	ventas=200
	mes=['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']
	lista_registros=[]
	registro={}
	registro['puesto']='Supervisor'
	registro['nombre']='Fulano de Tal'
	registro['numero_empleado']='69666420'
	registro['plaza']='Polanco'
	registro['fecha_ingreso']='01/12/2017'
	for x in mes:
		registro[x]=ventas
		ventas+=ventas
	registro['promedio']=round((ventas/12), 2)
	lista_registros.append(registro)
	lista_registros.append(registro)
	lista_registros.append(registro)
	registro['puesto']='Asesor'
	for x in mes:
		registro[x]=ventas
		ventas+=ventas
	registro['promedio']=round((ventas/12), 2)
	lista_registros.append(registro)
	lista_registros.append(registro)
	lista_registros.append(registro)
	return json.dumps(lista_registros)	
"""	
	
if __name__ == '__main__':	
	#si Rest.py
	app.run(host="127.0.0.1",debug=True, port=9999, threaded=True)



















    
	


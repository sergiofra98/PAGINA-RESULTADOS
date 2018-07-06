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
		print(id_periodo)		
		periodo += 1
		data_periodo = {}
		data_periodo['id_per'] = id_periodo
		data_periodo['per'] = id_periodo
		lista_periodos.append(data_periodo)
	return json.dumps(lista_periodos)
	
	
@app.route(url_base+'/vendedores',methods=['GET']) 
def vendedores():
	ventas=200
	mes=['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']
	lista_vendedores=[]
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
	lista_vendedores.append(registro)
	lista_vendedores.append(registro)
	lista_vendedores.append(registro)
	return json.dumps(lista_vendedores)

@app.route(url_base+'/division/<div>',methods=['GET']) 
def division(div):
	divs=['centro','sur','norte','noreste','vm_norte','vm_sur','vm_centro']
	if div in divs:
		print (div)#consulta por la division
	else:
		return 'Division no encontrada'
	lista_empresas=[]
	registro={}
	registro['contrato']='9879556558'
	registro['división']=div
	registro['convenio']='AMLO'
	registro['sucursal']='420'
	registro['fecha_disp']='01/01/2018'
	registro['monto_prestamo']=15000
	registro['monto_financiar']=2589.56
	registro['saldo_capital']=13500
	registro['int_dev_no_cob']=240
	registro['no_vendedor']='69666420'
	lista_empresas.append(registro)
	lista_empresas.append(registro)
	lista_empresas.append(registro)
	for i, x in enumerate(lista_empresas):
		lista_empresas[i]['saldo_contable'] = x['saldo_capital'] + x['int_dev_no_cob']
	return json.dumps(lista_empresas)


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
				 ['IMSS PARITARIA',2000,0,500],
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
			registro['total_mes_vs_ma_pct'] = '{:0,.2f}%'.format((row[1]/row[2]-1)*100) 
		if row[3] == 0:
			registro['total_mes_vs_maa_pct'] = '0.00%'
		else:
			registro['total_mes_vs_maa_pct'] = '{:0,.2f}%'.format((row[1]/row[3]-1)*100)
	
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
		registro_totales['total_mes_vs_ma_pct'] = '{:0,.2f}%'.format((total_mes/total_ma-1)*100) 
	if total_maa == 0:
		registro_totales['total_mes_vs_maa_pct'] = '0.00%'
	else:
		registro_totales['total_mes_vs_maa_pct'] = '{:0,.2f}%'.format((total_mes/total_maa-1)*100)
	
	lista_resultado.append(registro_totales)

	return json.dumps(lista_resultado)


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
	
	print(total_mes)
	print(total_mes_aa)
	print(total_acu)
	
	contador = 1
	for row in lista_datos:
		print(row)
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
	
	
	"""
	lista_empresas={}
	registro={}
	
	
	registro['colocacion_mes']=500000
	registro['colocacion_mes_aa']=250000
	registro['colocacion_acumulado']=6000000
	registro['cartera_mes_anterior']=2500
	registro['cartera_mes_actual']=5000
	registro['cartera_mes_anio_anterior']=2000
	lista_empresas['registros']=[]
	lista_empresas['registros'].append(registro)
	lista_empresas['registros'].append(registro)
	lista_empresas['registros'].append(registro)
	lista_empresas['registros'].append(registro)
	#Estos valores los sacamos en consulta ahorita son estaticos
	lista_empresas['colocacion_total_mes'] = 2000000
	lista_empresas['colocacion_total_mes_aa'] = 1000000
	lista_empresas['colocacion_total_acumulado'] = 24000000
	lista_empresas['cartera_total_mes_anterior']=10000
	lista_empresas['cartera_total_mes_actual']=20000
	lista_empresas['cartera_total_mes_anio_anterior']=8000
	#estos se pueden calcular en back o front
	lista_empresas['cartera_total_mes_actual_vs_mes_anterior']=lista_empresas['cartera_total_mes_actual']-lista_empresas['cartera_total_mes_anterior']
	lista_empresas['cartera_total_mes_actual_vs_anio_anterior']=lista_empresas['cartera_total_mes_actual']-lista_empresas['cartera_total_mes_anio_anterior']
	lista_empresas['cartera_porcentaje_mes_actual_vs_mes_anterior']=(lista_empresas['cartera_total_mes_actual']/lista_empresas['cartera_total_mes_anterior'])*100
	lista_empresas['cartera_procentaje_mes_actual_vs_anio_anterior']=(lista_empresas['cartera_total_mes_actual']/lista_empresas['cartera_total_mes_anio_anterior'])*100
	for i, x in enumerate(lista_empresas['registros']):
		lista_empresas['registros'][i]['colocacion_porcentaje_mes'] = (x['colocacion_mes'] / lista_empresas['colocacion_total_mes'])*100
		lista_empresas['registros'][i]['colocacion_porcentaje_mes_aa'] = (x['colocacion_mes_aa'] / lista_empresas['colocacion_total_mes_aa'])*100
		lista_empresas['registros'][i]['colocacion_porcentaje_acumulado'] = (x['colocacion_acumulado'] / lista_empresas['colocacion_total_acumulado'])*100
		lista_empresas['registros'][i]['cartera_vs_porcentaje_mes_anterior'] = (x['cartera_mes_actual'] / x['cartera_mes_anterior'])*100
		lista_empresas['registros'][i]['cartera_vs_porcentaje_anio_anterior'] = (x['cartera_mes_actual'] / x['cartera_mes_anio_anterior'])*100
		lista_empresas['registros'][i]['cartera_vs_mes_anterior'] = x['cartera_mes_actual'] - x['cartera_mes_anterior']
		lista_empresas['registros'][i]['cartera_vs_anio_anterior'] = x['cartera_mes_actual'] - x['cartera_mes_anio_anterior']
	"""
	return json.dumps(lista_resultado)

if __name__ == '__main__':	
	#si Rest.py
	app.run(host="127.0.0.1",debug=True, port=9999, threaded=True)



















    
	


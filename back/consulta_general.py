#encoding=utf-8
from google.cloud import bigquery
from big_query_conexion import obtener_datos


import uuid
import time
import csv  
import sys
import traceback
import string
import os
import locale

locale.setlocale(locale.LC_ALL, '')
reload(sys)
sys.setdefaultencoding('utf8')
v_legacy_sql = False

def consulta_divisiones():
	data = {} 
	sql	= " select division, nombre from BUO_Masnomina.masnomina_divisiones order by nombre "
	print sql
	query_parameters =()
	rows = obtener_datos(sql, v_legacy_sql, query_parameters)
	print rows
	lista_divisiones = []
	if rows != None:
		for row in rows:
			division={}
			division['id_div'] = row[0]
			division['nombre'] = row[1]
			lista_divisiones.append(division)
	data = lista_divisiones
	return data
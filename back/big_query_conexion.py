from google.cloud import bigquery

import variables
import uuid
import time
import csv  
import sys
import traceback
import string
import os
import locale


def obtener_datos(query, legacy_sql, query_parameters):
	try:
		credentialsBG = os.getcwd() + "\service-mn@desarrollo-ci.iam.gserviceaccount-c04f8c.json" #se establece la ruta de las credenciales
		os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentialsBG #asignamos la ruta de las credenciales a entorno de Google pra python
		
		cliente = bigquery.Client.from_service_account_json(variables.bq_json)
		job_name = str(uuid.uuid4())
		query_job = cliente.run_async_query(job_name, query, query_parameters)
		query_job.use_legacy_sql = legacy_sql
		query_job.begin()
		wait_for_job(query_job)
		query_results = query_job.results()
		rows, total_rows, page_token = query_results.fetch_data()
		page_token = None
		while True:
			print "****page****"
			rows,total_rows,page_token = query_results.fetch_data(max_results=10000, page_token=page_token)
			print "rows " , len(rows)
			print "total_rows " , total_rows
			print "page_token " , page_token
			if not page_token:
				break
		return rows
	except:
		print 'Error en obtener datos Big Query :',  sys.exc_info()
		print traceback.format_exc()

def obtener_datos_ser(query, legacy_sql, query_parameters):
	try:
		cliente = bigquery.Client.from_service_account_json(variables.bq_json);
		job_name = str(uuid.uuid4())
		query_job = cliente.run_async_query(job_name, query, query_parameters)
		query_job.use_legacy_sql = legacy_sql
		query_job.begin()
		wait_for_job(query_job)
		query_results = query_job.results()
		rows = query_results.fetch_data()
		return rows
	except:
		print 'Error en obtener datos Big Query :',  sys.exc_info()
		print traceback.format_exc()

def wait_for_job(job):
	"""Realiza una espera para asegurar que el job se ha ejecutado correctamente."""
	while True:
		job.reload()
		if job.state == 'DONE':
			if job.error_result:
				raise RuntimeError(job.errors)
			return
		time.sleep(1)

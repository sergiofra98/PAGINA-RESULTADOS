# # -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from functools import reduce
from consulta_general import consulta_divisiones
from big_query_conexion import obtener_datos
import json
import datetime
import locale

locale.setlocale(locale.LC_ALL, '')
app = Flask(__name__)
PORT = 9996
DEBUG = True
IP = "10.1.50.149"


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


url_base = '/MasNomina/MonitorVentas'


def formatear_no_mes(mes):
    if(mes < 10):
        return '0' + str(mes)
    else:
        return str(mes)


@app.route(url_base)
def hello():
    return "Monitor Ventas Estatus[OK]"


# combo box de divisiones
@app.route(url_base+'/consulta_anios', methods=['GET'])
def f_consulta_anios():
    lista_anios = []
    anio = {}
    anio['id_anio'] = 2018
    lista_anios.append(anio)
    anio = {}
    anio['id_anio'] = 2017
    lista_anios.append(anio)
    return json.dumps(lista_anios)

# combo box de divisiones


@app.route(url_base+'/consulta_divisiones', methods=['GET'])
def f_consulta_divisiones():
    registros = consulta_divisiones()
    return json.dumps(registros)


# combo box de periodos
@app.route(url_base+'/consulta_periodos', methods=['GET'])
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
                anio = anio - 1
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


@app.route(url_base+'/consulta_convenio_colocacion', methods=['GET'])
def consulta_convenio_colocacion():
    division = request.args.get('division')
    mes = request.args.get('mes')
    producto = request.args.get('producto')

    mes_numero = int(mes[4] + mes[5])
    anio = int(mes[0] + mes[1] + mes[2] + mes[3])

    # SE GENERA EL QUERY
    # SE GENERA EL QUERY
    # SE GENERA EL QUERY
    query_convenio = """select
    case
        when universo_2.clave_corresponsal is null then aa.clave_corresponsal
        else universo_2.clave_corresponsal
    end as clave_corresponsal,
    case
        when universo_2.razon_social is null then aa.razon_social
        else universo_2.razon_social
    end as razon_social,
    ifnull(universo_2.monto_dispuesto,0) as monto_dispuesto,
    ifnull(universo_2.monto_dispuesto_ma,0) as monto_dispuesto_ma,
    ifnull(universo_2.monto_dispuesto_acu,0) as monto_dispuesto_acu,
    ifnull(aa.monto_dispuesto_acu_aa,0) as monto_dispuesto_acu_aa
    from (
    select
        case
            when universo_1.clave_corresponsal is null then mes_acumulado.clave_corresponsal
            else universo_1.clave_corresponsal
        end as clave_corresponsal,
        case
            when universo_1.razon_social is null then  mes_acumulado.razon_social
            else universo_1.razon_social
        end as razon_social,
        ifnull(universo_1.monto_dispuesto,0) as monto_dispuesto,
        ifnull(universo_1.monto_dispuesto_ma,0)  as monto_dispuesto_ma,
        ifnull(mes_acumulado.monto_dispuesto_acu,0) as monto_dispuesto_acu
    from (
            select case
                    when mes_actual.clave_corresponsal is null then mes_anterior.clave_corresponsal
                    else mes_actual.clave_corresponsal
                end as clave_corresponsal,
                case
                    when mes_actual.razon_social is null then mes_anterior.razon_social
                    else  mes_actual.razon_social
                end as razon_social,
                ifnull(mes_actual.monto_dispuesto,0) as monto_dispuesto,
                ifnull(mes_anterior.monto_dispuesto,0) as monto_dispuesto_ma
            from (
            select clave_corresponsal, razon_social, sum(monto_dispuesto) as monto_dispuesto
            from BUO_Masnomina.contratos_hist """
    if(mes_numero == 12):
        query_convenio += "where fecha_disposicion >= '" + \
            str(anio) + "-" + formatear_no_mes(mes_numero) + \
            "-01' and fecha_disposicion < '" + str(anio + 1) + "-01-01' "
    else:
        query_convenio += "where fecha_disposicion >= '" + str(anio) + "-" + formatear_no_mes(
            mes_numero) + "-01' and fecha_disposicion < '" + str(anio) + "-" + formatear_no_mes(mes_numero + 1) + "-01' "
    query_convenio += "and mes = " + mes + " "
    if(int(division)):
        query_convenio += "and division = " + division + " "
    if(producto == "0"):
        query_convenio += "/*and producto = '" + producto + "'*/ "
    query_convenio += """ group by clave_corresponsal, razon_social
        ) mes_actual
        full join (
          select clave_corresponsal, razon_social, sum(monto_dispuesto) as monto_dispuesto
          from BUO_Masnomina.contratos_hist """
    if(mes_numero == 12):
        query_convenio += "where fecha_disposicion >= '" + \
            str(anio - 1) + "-" + formatear_no_mes(mes_numero) + \
            "-01' and fecha_disposicion < '" + str(anio) + "-01-01' "
    else:
        query_convenio += "where fecha_disposicion >= '" + str(anio - 1) + "-" + formatear_no_mes(
            mes_numero) + "-01' and fecha_disposicion < '" + str(anio - 1) + "-" + formatear_no_mes(mes_numero+1) + "-01' "
    query_convenio += "and mes = " + \
        str(anio - 1) + formatear_no_mes(mes_numero) + " "
    if(int(division)):
        query_convenio += "and division = " + division + " "
    if(producto == "0"):
        query_convenio += "/*and producto = '" + producto + "'*/ "
    query_convenio += """ group by clave_corresponsal, razon_social
            ) mes_anterior on mes_anterior.clave_corresponsal = mes_actual.clave_corresponsal
    ) universo_1
    full join (
            select contratos.clave_corresponsal, contratos.razon_social, sum(contratos.monto_dispuesto) as monto_dispuesto_acu
            from (
            select distinct clave_corresponsal, razon_social, contrato, monto_dispuesto
            from BUO_Masnomina.contratos_hist """
    if(mes_numero == 12):
        query_convenio += "where fecha_disposicion >= '" + \
            str(anio) + "-01-01' and fecha_disposicion < '" + \
            str(anio) + "-01-01' "
    else:
        query_convenio += "where fecha_disposicion >= '" + \
            str(anio) + "-01-01' and fecha_disposicion < '" + \
            str(anio + 1) + "-" + formatear_no_mes(mes_numero + 1) + "-01' "
    query_convenio += "and mes >= " + \
        str(anio) + "01 and mes <= " + mes + " "
    if(int(division)):
        query_convenio += "and division = " + division + " "
    if(producto == "0"):
        query_convenio += "/*and producto = '" + producto + "'*/ "
    query_convenio += """ ) contratos
            group by contratos.clave_corresponsal, contratos.razon_social
    ) mes_acumulado on mes_acumulado.clave_corresponsal = universo_1.clave_corresponsal
    ) universo_2
    full join (
        select contratos.clave_corresponsal, contratos.razon_social, sum(contratos.monto_dispuesto) as monto_dispuesto_acu_aa
        from (
            select distinct clave_corresponsal, razon_social, contrato, monto_dispuesto
            from BUO_Masnomina.contratos_hist """
    if(mes_numero == 12):
        query_convenio += "where fecha_disposicion >= '" + \
            str(anio - 1) + "-01-01' and fecha_disposicion < '" + \
            str(anio) + "-01-01' "
    else:
        query_convenio += "where fecha_disposicion >= '" + \
            str(anio - 1) + "-01-01' and fecha_disposicion < '" + \
            str(anio - 1) + "-" + formatear_no_mes(mes_numero + 1) + "-01' "
    query_convenio += "and mes >= " + \
        str(anio - 1) + "01 and mes <= " + str(anio - 1) + \
        formatear_no_mes(mes_numero) + " "
    if(int(division)):
        query_convenio += "and division = " + division + " "
    if(producto == "0"):
        query_convenio += "/*and producto = '" + producto + "'*/ "
    query_convenio += """ ) contratos
        group by contratos.clave_corresponsal, contratos.razon_social
    ) aa on aa.clave_corresponsal = universo_2.clave_corresponsal
    order by 3 desc """

    # se realiza la consulta

    lista_datos = []

    lista_datos = obtener_datos(query_convenio, False, ())

    if(not len(lista_datos)):
        return json.dumps({})

    tempTotal = {}
    tempTotal['nombre'] = 'TOTAL'
    tempTotal['total_mes'] = 0
    tempTotal['total_mes_aa'] = 0
    tempTotal['total_acu'] = 0
    tempTotal['total_acu_aa'] = 0
    tempTotal['total_mes_aa_pct'] = '100%'
    tempTotal['total_mes_pct'] = '100'

    for row in lista_datos:
        tempTotal['total_mes'] += row[2]
        tempTotal['total_mes_aa'] += row[3]
        tempTotal['total_acu'] += row[4]
        tempTotal['total_acu_aa'] += row[5]
    
    if (not tempTotal['total_mes'] or not tempTotal['total_mes_aa'] or not tempTotal['total_acu'] or not tempTotal['total_acu_aa']):
        return json.dumps({})

    if(tempTotal['total_acu_aa'] != 0):
        tempTotal['total_acu_comp_pct'] = '{:0,.1f}'.format(
            ((tempTotal['total_acu'] - tempTotal['total_acu_aa']) / tempTotal['total_acu_aa']) * 100.00)
    else:
        tempTotal['total_acu_comp_pct'] = '∞'

    if(tempTotal['total_acu_comp_pct'] == '-100.0'):
        tempTotal['total_acu_comp_pct'] = '-∞'

    if(tempTotal['total_acu_comp_pct'][0] == '-'):
        tempTotal['color_acu'] = 'rojo'
    else:
        tempTotal['color_acu'] = ''

    lista_resultado = []

    for row in lista_datos:
        temp = {}
        temp['nombre'] = row[1]
        temp['total_mes'] = '{:0,.2f}'.format(row[2])
        temp['total_mes_aa'] = '{:0,.2f}'.format(row[3])
        temp['total_acu'] = '{:0,.2f}'.format(row[4])
        temp['total_acu_aa'] = '{:0,.2f}'.format(row[5])

        temp['total_mes_pct'] = '{:0,.1f}'.format(
            (row[2]/tempTotal['total_mes'])*100)
        temp['total_mes_aa_pct'] = '{:0,.1f}'.format(
            (row[3]/tempTotal['total_mes_aa'])*100)

        if(row[5] != 0):
            temp['total_acu_comp_pct'] = '{:0,.1f}'.format(
                ((row[4] - row[5]) / row[5]) * 100.00)
        else:
            temp['total_acu_comp_pct'] = '∞'

        if(temp['total_acu_comp_pct'] == '-100.0'):
            temp['total_acu_comp_pct'] = '-∞'

        if(temp['total_acu_comp_pct'][0] == '-'):
            temp['color_acu'] = 'rojo'
        else:
            temp['color_acu'] = ''

        lista_resultado.append(temp)

    tempTotal['total_mes'] = '{:0,.2f}'.format(tempTotal['total_mes'])
    tempTotal['total_mes_aa'] = '{:0,.2f}'.format(tempTotal['total_mes_aa'])
    tempTotal['total_acu'] = '{:0,.2f}'.format(tempTotal['total_acu'])
    tempTotal['total_acu_aa'] = '{:0,.2f}'.format(tempTotal['total_acu_aa'])

    lista_resultado.append(tempTotal)

    return json.dumps(lista_resultado)

# tabla x convenio cartera


@app.route(url_base+'/consulta_convenio_cartera', methods=['GET'])
def consulta_convenio_cartera():
    division = request.args.get('division')
    mes = request.args.get('mes')
    producto = request.args.get('producto')

    mes_numero = int(mes[4] + mes[5])
    anio = int(mes[0] + mes[1] + mes[2] + mes[3])
    lista_meses = [	'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul',
                    'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

    # se realiza la consulta
    lista_resultado = {}

    lista_mes = [lista_meses[mes_numero-1]+' ' + str(anio-1), lista_meses[mes_numero-2]+' ' + str(anio), lista_meses[mes_numero-1]+' ' + str(anio)]
    # [mes actual, mes anterior, mes año anterior]

    query_convenio_cartera="""select
        case
            when universo_1.clave_corresponsal is null then mact_aa.clave_corresponsal
            else universo_1.clave_corresponsal
        end as clave_corresponsal,
        case
            when universo_1.razon_social is null then mact_aa.razon_social
            else universo_1.razon_social
        end as razon_social,
        ifnull(universo_1.saldo_contable_mact,0) as saldo_contable_mact,
        ifnull(universo_1.saldo_contable_mant,0) as saldo_contable_mant,
        ifnull(mact_aa.saldo_contable_mact_aa,0) as saldo_contable_mact_aa
    from (
        select
        case
            when mact.clave_corresponsal is null then mant.clave_corresponsal
            else mact.clave_corresponsal
        end as clave_corresponsal,
        case
            when mact.razon_social is null then  mant.razon_social
            else mact.razon_social
        end as razon_social,
        ifnull(mact.saldo_contable_mact,0) as saldo_contable_mact,
        ifnull(mant.saldo_contable_mant,0) as saldo_contable_mant
        from (
            select
            clave_corresponsal, razon_social, sum(saldo_contable) as saldo_contable_mact
            from BUO_Masnomina.contratos_hist
            where 1 = 1 """
    query_convenio_cartera += "and mes = " + mes + " "
    if(int(division)):
        query_convenio_cartera += "and division = " + division + " "
    query_convenio_cartera += "and estatus_contable in ('VIG','VEN') "
    if(producto == "0"):
        query_convenio_cartera += "/*and producto = '" + producto + "'*/ "
    query_convenio_cartera += """group by clave_corresponsal, razon_social
        ) mact
    full join
      (
        select clave_corresponsal, razon_social, sum(saldo_contable) as saldo_contable_mant
        from BUO_Masnomina.contratos_hist
        where 1 = 1 """
    if(mes_numero == 1):
        query_convenio_cartera += "and mes = " + str(anio-1) + "12 "
    else:
        query_convenio_cartera += "and mes = " + \
            str(anio) + formatear_no_mes(mes_numero - 1) + " "
    if(int(division)):
        query_convenio_cartera += "and division = " + division + " "
    query_convenio_cartera += "and estatus_contable in ('VIG','VEN') "
    if(producto == "0"):
        query_convenio_cartera += "/*and producto = '" + producto + "'*/ "
    query_convenio_cartera += """group by clave_corresponsal, razon_social
            ) mant on mant.clave_corresponsal = mact.clave_corresponsal
    ) universo_1
    full join (
        select clave_corresponsal, razon_social, sum(saldo_contable) as saldo_contable_mact_aa
        from BUO_Masnomina.contratos_hist
        where 1 = 1 """
    query_convenio_cartera += "and mes = " + \
        str(anio-1) + formatear_no_mes(mes_numero) + " "
    if(int(division)):
        query_convenio_cartera += "and division = " + division + " "
    query_convenio_cartera += "and estatus_contable in ('VIG','VEN') "
    if(producto == "0"):
        query_convenio_cartera += "/*and producto = '" + producto + "'*/ "
    query_convenio_cartera += """group by clave_corresponsal, razon_social
    ) mact_aa on mact_aa.clave_corresponsal = universo_1.clave_corresponsal
    order by 3 desc"""

    lista_datos=obtener_datos(query_convenio_cartera, False, ())

    if(not len(lista_datos)):
        return json.dumps({})

    lista_resultado['cartera']=[]
    lista_resultado['meses']=lista_mes

    # Obtenemos totales
    total_mes=0
    total_ma=0
    total_maa=0
    # de esto podriamos hacer una consulta a DB con un SUM para quitarle carga al back
    # ya que si es mucha informacion la que se va a sacar entonces esta iteracion lo hara
    # más lento
    for row in lista_datos:
        total_mes += row[2]
        total_ma += row[3]
        total_maa += row[4]

    for row in lista_datos:

        registro={}
        registro['nombre']=row[1]

        registro['total_mes']='{:0,.0f}'.format(row[2])
        registro['total_ma']='{:0,.0f}'.format(row[3])
        registro['total_maa']='{:0,.0f}'.format(row[4])

        registro['total_mes_vs_ma']='{:0,.0f}'.format(row[2]-row[3])
        registro['total_mes_vs_maa']='{:0,.0f}'.format(row[2]-row[4])

        if row[3] == 0:
            registro['total_mes_vs_ma_pct']='0.00%'
        else:
            pct_m_ma=0
            pct_m_ma=(row[2] * 1.00) / (row[3] * 1.00) - 1
            pct_m_ma=pct_m_ma * 100.00
            registro['total_mes_vs_ma_pct']='{:0,.2f}%'.format(pct_m_ma)

            if pct_m_ma < 0:
                registro['colorMA']="rojo"
            else:
                registro['colorMA']="blanco"
        if row[4] == 0:
            registro['total_mes_vs_maa_pct']='0.00%'
        else:
            pct_m_maa=0
            if row[2] == 0:
                pct_m_maa=0
            else:
                pct_m_maa=(row[4] * 1.00) / (row[2] * 1.00) - 1
            pct_m_maa=pct_m_maa * 100.00
            registro['total_mes_vs_maa_pct']='{:0,.2f}%'.format(pct_m_maa)

            if pct_m_maa < 0:
                registro['colorMAA']="rojo"
            else:
                registro['colorMAA']="blanco"

        lista_resultado['cartera'].append(registro)

    registro_totales={}
    registro_totales['nombre']='TOTAL'

    registro_totales['total_mes']='{:0,.0f}'.format(total_mes)
    registro_totales['total_ma']='{:0,.0f}'.format(total_ma)
    registro_totales['total_maa']='{:0,.0f}'.format(total_maa)

    registro_totales['total_mes_vs_ma']='{:0,.0f}'.format(total_mes-total_ma)
    registro_totales['total_mes_vs_maa']='{:0,.0f}'.format(
        total_maa-total_mes)

    if total_ma == 0:
        registro_totales['total_mes_vs_ma_pct']='0.00%'
    else:
        registro_totales['total_mes_vs_ma_pct']='{:0,.2f}%'.format(
            ((total_mes * 1.00) / (total_ma * 1.00)-1)*100)
        polaridad=((total_mes * 1.00) / (total_ma * 1.00)-1)*100
        if polaridad < 0:
            registro_totales['colorMA']="rojo"
        else:
            registro_totales['colorMA']="blanco"
    if total_maa == 0:
        registro_totales['total_mes_vs_maa_pct']='0.00%'
    else:
        polaridad=((total_maa * 1.00) / (total_mes * 1.00)-1)*100
        registro_totales['total_mes_vs_maa_pct']='{:0,.2f}%'.format(
            ((total_maa * 1.00) / (total_mes * 1.00)-1)*100)
        if polaridad < 0:
            registro_totales['colorMAA']="rojo"
        else:
            registro_totales['colorMAA']="blanco"

    lista_resultado['cartera'].append(registro_totales)

    return json.dumps(lista_resultado)

def juntar_tablas(arregloInicial):
    Universo = []

    for tabla in arregloInicial:
        for fila in tabla:
            if fila[0] not in Universo:
                Universo.append(fila[0])

    for tabla in arregloInicial:
        elementos = []

        for fila in tabla:
            elementos.append([fila[0], fila[1]])
        for entidad in Universo:
            if entidad not in elementos:
                tabla.append((entidad[0], 0))

    for tabla in arregloInicial:
        tabla.sort()

    Universo.sort()

    retornoTabla = []

    for i, elem in enumerate(Universo):
        aux = []
        aux.append(elem[1])

        for tabla in arregloInicial:
            aux.append(tabla[i][2])

        retornoTabla.append(aux)

    return retornoTabla


# tabla venta x estado
@app.route(url_base+'/consulta_estado_colocacion', methods = ['GET'])
def consulta_estado_colocacion():
    division=request.args.get('division')
    mes=request.args.get('mes')
    producto=request.args.get('producto')

    mes_numero =int(mes[4] + mes[5])
    anio =int(mes[0] + mes[1] + mes[2] + mes[3])

    lista_estados_todos=[]
    lista_estados_asesores=[]
    lista_estados_supervisores=[]
    lista_meses = []

    lista_retorno = {}
    nombres_meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul',
                    'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

    query_supervisor="""select p.mes, s.estado, count(*)
    from BUO_Masnomina.masnomina_plantilla p
    left join BUO_Masnomina.masnomina_sucursales s on s.sucursal = p.sucursal
    where 1 = 1 and  
    p.puesto = 'SUPERVISOR COMERCIAL MAS NOMINA' """
    query_supervisor += "and p.mes >= "+ str(anio-1) + formatear_no_mes(mes_numero) +" and p.mes <= "+ str(anio) + formatear_no_mes(mes_numero) +" "
    if(int(division)):
        query_supervisor += "and s.division = " + division + " "
    query_supervisor += "group by p.mes, s.estado order by p.mes, s.estado"

    query_asesor="""select p.mes, s.estado, count(*)
    from BUO_Masnomina.masnomina_plantilla p
    left join BUO_Masnomina.masnomina_sucursales s on s.sucursal = p.sucursal
    where 1 = 1 and  
    p.puesto = 'ASESOR MAS NOMINA' """
    query_asesor += "and p.mes >= "+ str(anio-1) + formatear_no_mes(mes_numero) +" and p.mes <= "+ str(anio) + formatear_no_mes(mes_numero) +" "
    if(int(division)):
        query_asesor += "and s.division = " + division + " "
    query_asesor += "group by p.mes, s.estado order by p.mes, s.estado"


    lista_estados_asesores.append(obtener_datos(query_asesor, False, ()))
    lista_estados_supervisores.append(obtener_datos(query_supervisor, False, ()))

    for i in range(13):
        no_mes=mes_numero - i
        sobreflujo=False

        if(no_mes < 1):
            sobreflujo=True

        # SE GENERAN LOS MESES
        if(sobreflujo):
            lista_meses.append( nombres_meses[no_mes + 11] + ' ' + str(anio-1))
        else:
            lista_meses.append( nombres_meses[no_mes -1] + ' ' +  str(anio))

        # SE HACE EL QUERY DE ESTADO
        query_estado="""select s.estado, sum(c.monto_dispuesto) as monto
        from BUO_Masnomina.contratos_hist c
        left join BUO_Masnomina.masnomina_sucursales s on s.sucursal = c.sucursal
        where 1 = 1 """
        if(sobreflujo):
            if(no_mes == 0):
                query_estado += "and c.fecha_disposicion >= '" + \
                    str(anio - 1)+"-12-01' and c.fecha_disposicion < '" + \
                    str(anio)+"-01-01' "
            else:
                query_estado += "and c.fecha_disposicion >= '" + str(anio - 1)+"-" + formatear_no_mes(
                    12 + no_mes) + "-01' and c.fecha_disposicion < '" + str(anio - 1)+"-" + formatear_no_mes(13 + no_mes) + "-01' "
            query_estado += "and c.mes = " + str(anio - 1) + formatear_no_mes(12 + no_mes) + " "
        else:
            if(no_mes == 12):
                query_estado += "and c.fecha_disposicion >= '" + str(anio)+"-12-01' and c.fecha_disposicion < '" + str(anio+1)+"-01-01' "
            else:
                query_estado += "and c.fecha_disposicion >= '" + str(anio)+"-" + formatear_no_mes(
                    no_mes) + "-01' and c.fecha_disposicion < '" + str(anio)+"-" + formatear_no_mes(no_mes+1) + "-01' "
            query_estado += "and c.mes = " + str(anio) + formatear_no_mes(no_mes) + " "
        if(int(division)):
            query_estado += "and c.division = " + division + " "
        query_estado += "group by s.estado order by 1"
        lista_estados_todos.append(obtener_datos(query_estado, False, ()))
        
    lista_estados_supervisores = arreglar_tablas(arreglar_tablas_empleados(lista_estados_supervisores, mes_numero, anio), mes_numero)
    lista_estados_asesores =arreglar_tablas(arreglar_tablas_empleados(lista_estados_asesores, mes_numero, anio), mes_numero)
    lista_estados_todos = arreglar_tablas(lista_estados_todos, mes_numero)
    lista_promedio_asesores = formatear_dinero(calcular_promedios(lista_estados_todos, lista_estados_asesores))
    lista_promedio_supervisores = formatear_dinero(calcular_promedios(lista_estados_todos, lista_estados_supervisores))


    lista_retorno['estados'] = formatear_dinero(lista_estados_todos)
    lista_retorno['lista_supervisores'] = lista_estados_supervisores
    lista_retorno['lista_asesores'] = lista_estados_asesores
    lista_retorno['lista_asesores_promedio'] = lista_promedio_asesores
    lista_retorno['lista_supervisores_promedio'] = lista_promedio_supervisores
    lista_retorno['meses'] = lista_meses

   
    return json.dumps(lista_retorno)

def arreglar_tablas(arregloInicial, contador_mes):
    Universo = []
    for tabla in arregloInicial:
        for fila in tabla:
            if fila[0] not in Universo:
                Universo.append(fila[0])

    for i,tabla in enumerate(arregloInicial):
        elementos = []
        for fila in tabla:
            elementos.append(fila[0])        
        for entidad in Universo:
            if entidad not in elementos:
                tabla.append((entidad, 0))
        tabla.sort()

    retorno = [None]*len(arregloInicial[0])


    for i in range(len(arregloInicial[0])):
        total = 0
        totalA = 0
        totalAA = 0
        retorno[i] = []
        retorno[i].append(arregloInicial[0][i][0])
        for j in range(13):
            if(j < contador_mes):
                totalA +=arregloInicial[j][i][1]
            else:
                totalAA +=arregloInicial[j][i][1]
            total += arregloInicial[j][i][1]
            retorno[i].append(arregloInicial[j][i][1])
        retorno[i].append(totalA)
        retorno[i].append(totalAA)
        retorno[i].append(total)

    totalMes = []
    totalMes.append('TOTAL')

    for i in range(1, len(retorno[0])):
        aux = 0
        for j in range(len(retorno)):
            aux += retorno[j][i]
        totalMes.append(aux)

    retorno.append(totalMes)

    return retorno

def calcular_promedios(arregloEstados, arregloEmpleados):
    arregloPromedio = []

    for row01 in arregloEmpleados:
        aux = []
        for row02 in arregloEstados:
            if(row01[0] == row02[0]):
                aux.append(row01[0])
                for i in range(1, len(row01)):
                    if(row01[i]):
                        aux.append(row02[i]/row01[i])
                    else:
                        aux.append(0)
                break
        arregloPromedio.append(aux)
    
    return arregloPromedio

def arreglar_tablas_empleados(arregloInicial, mes, anio):
    arregloFinal = []
    temp = arregloInicial.pop()

    sobreflujo = False
    for i in range(13):
        mes_num = mes - i
        
        aux = []
        aux2 = []

        if(mes_num == 0):
            sobreflujo = True

        if(sobreflujo):
            aux = filter(lambda  x: x[0] == (int(str(anio-1) + formatear_no_mes(mes_num+12))), temp)
        else:
            aux = filter(lambda  x: x[0] == (int(str(anio) + formatear_no_mes(mes_num))), temp)

        for element in aux:
            element = list(element)
            element.pop(0)
            aux2.append(element)
        arregloFinal.append(aux2)
    
    return arregloFinal

def formatear_dinero(arregloInicial):
    for row in arregloInicial:
        for i in range(1, len(row)):
            row[i] = '{:0,.2f}'.format(row[i])
    return arregloInicial


@app.route(url_base+'/costos_colocacion', methods=['GET'])
def costos_colocacion():
    division = request.args.get('division')
    mes = request.args.get('mes')
    producto = request.args.get('producto')

    # SE SEPARA LA FECHA EN SUS RESPECTIVAS PARTES
    mes_numero = int(mes[4] + mes[5])
    anio = int(mes[0] + mes[1] + mes[2] + mes[3])

    # SE GENERA EL PRIMER QUERYYY
    query01 = """select colmen.colocacion, 
    col.comisiones, col.sueldo_fijo, col.carga_social_aguinaldo, col.viaticos, col.gasolina, col.costos_autos, col.rentas,
    (col.comisiones + col.sueldo_fijo + col.carga_social_aguinaldo + col.viaticos + col.gasolina + col.costos_autos + col.rentas) as total,
    round((col.comisiones / colmen.colocacion) * 100,2) as pct_comisiones,
    round((col.sueldo_fijo / colmen.colocacion) * 100,2) as pct_sueldo_fijo,
    round((col.carga_social_aguinaldo / colmen.colocacion) * 100,2) as pct_carga_social_aguinaldo,
    round((col.viaticos / colmen.colocacion) * 100,2) as pct_viaticos,
    round((col.gasolina / colmen.colocacion) * 100,2) as pct_gasolina,
    round((col.costos_autos / colmen.colocacion) * 100,2) as pct_costos_autos,
    round((col.rentas / colmen.colocacion) * 100,2) as pct_rentas,
    round(((col.comisiones + col.sueldo_fijo + col.carga_social_aguinaldo + col.viaticos + col.gasolina + col.costos_autos + col.rentas) / colmen.colocacion) * 100,2) as pct_total
    from BUO_Masnomina.costo_colocacion_hist col,
    (
    select  ifnull(sum(monto_dispuesto),0) as colocacion
    from BUO_Masnomina.contratos_hist   
    where 1 = 1 
    /* aqui va el rango del mes seleccionado */ """
    query01 += "and fecha_disposicion >= '" + \
        str(anio) + "-" + formatear_no_mes(mes_numero) + "-01' "
    if(mes_numero == 12):
        query01 += "and fecha_disposicion < '" + str(anio + 1) + "-01-01' "
    else:
        query01 += "and fecha_disposicion < '" + \
            str(anio) + "-" + formatear_no_mes(mes_numero+1) + "-01' "

    query01 += "and mes = " + mes + " "
    if(int(division)):
        query01 += "and division = " + division + " "
    if(producto != "0"):
        query01 += "and producto = '" + producto + "' "
    query01 += """ ) colmen
    where 1 = 1
    /* mes seleccionado */"""
    query01 += " and col.mes = " + mes + "  "
    if(int(division)):
        query01 += " and col.division = " + division

    # SE ESCRIBE EL SEGUndO QUERY

    query02 = """select col_acum.colocacion, 
    acum.comisiones, acum.sueldo_fijo, acum.carga_social_aguinaldo, acum.viaticos, acum.gasolina, acum.costos_autos, acum.rentas,
    acum.total,
    round((acum.comisiones / col_acum.colocacion) * 100,2) as pct_comisiones,
    round((acum.sueldo_fijo / col_acum.colocacion) * 100,2) as pct_sueldo_fijo,
    round((acum.carga_social_aguinaldo / col_acum.colocacion) * 100,2) as pct_carga_social_aguinaldo,
    round((acum.viaticos / col_acum.colocacion) * 100,2) as pct_viaticos,
    round((acum.gasolina / col_acum.colocacion) * 100,2) as pct_gasolina,
    round((acum.costos_autos / col_acum.colocacion) * 100,2) as pct_costos_autos,
    round((acum.rentas / col_acum.colocacion) * 100,2) as pct_rentas,
    round(((acum.total) / col_acum.colocacion) * 100,2) as pct_total
    from
    (
    select  sum(col.comisiones) as comisiones , sum(col.sueldo_fijo) as sueldo_fijo, sum(col.carga_social_aguinaldo) as carga_social_aguinaldo, 
            sum(col.viaticos) as viaticos, sum(col.gasolina) as gasolina, sum(col.costos_autos) as costos_autos, sum(col.rentas) as rentas, 
            sum(col.comisiones) + sum(col.sueldo_fijo) + sum(col.carga_social_aguinaldo) + 
            sum(col.viaticos) + sum(col.gasolina) + sum(col.costos_autos) + sum(col.rentas) as total        
    from BUO_Masnomina.costo_colocacion_hist col
    where 1 = 1 """
    query02 += "and col.mes >= " + str(anio) + "01 and col.mes < " + mes + "  "
    if(int(division)):
        query02 += "and col.division = " + division + " "
    query02 += """) acum,
    (
    select ifnull(sum(contratos.monto_dispuesto),0) as colocacion
    from (
        select distinct contrato, monto_dispuesto
        from BUO_Masnomina.contratos_hist 
        /* aqui va el rango de enero al mes seleccionado */ """
    if(mes_numero == 12):
        query02 += "where fecha_disposicion >= '" + \
            str(anio) + "-01-01' and fecha_disposicion < '" + \
            str(anio + 1) + "-01-01' "
    else:
        query02 += "where fecha_disposicion >= '" + \
            str(anio) + "-01-01' and fecha_disposicion < '" + str(anio) + \
            "-" + formatear_no_mes(mes_numero + 1) + "-01' "

    query02 += "and mes >= " + str(anio) + "01 and mes < " + mes + " "

    if(int(division)):
        query02 += "and division = " + division + " "
    if(producto != "0"):
        query02 += "and producto = '" + producto + "' "
    query02 += """ ) contratos
    ) col_acum """

    lista_mes = obtener_datos(query01, False, ())

    lista_acumulado = obtener_datos(query02, False, ())

    if(len(lista_mes)):
        lista_mes = [	['Colocación',  '$ {:0,.2f}'.format(lista_mes[0][0]), '%'],
                      ['Comisiones',  '$ {:0,.2f}'.format(
                          lista_mes[0][1]), '{:0,.2f}%'.format(lista_mes[0][9])],
                      ['Sueldos fijo',  '$ {:0,.2f}'.format(
                          lista_mes[0][2]), '{:0,.2f}%'.format(lista_mes[0][10])],
                      ['Carga social + aguinaldo',  '$ {:0,.2f}'.format(
                          lista_mes[0][3]), '{:0,.2f}%'.format(lista_mes[0][11])],
                      ['Viáticos',  '$ {:0,.2f}'.format(
                          lista_mes[0][4]), '{:0,.2f}%'.format(lista_mes[0][12])],
                      ['Gasolina',  '$ {:0,.2f}'.format(
                          lista_mes[0][5]), '{:0,.2f}%'.format(lista_mes[0][13])],
                      ['Costo autos',  '$ {:0,.2f}'.format(
                          lista_mes[0][6]), '{:0,.2f}%'.format(lista_mes[0][14])],
                      ['Rentas',  '$ {:0,.2f}'.format(
                          lista_mes[0][7]), '{:0,.2f}%'.format(lista_mes[0][15])],
                      ['TOTAL',  '$ {:0,.2f}'.format(
                          lista_mes[0][8]), '{:0,.2f}%'.format(lista_mes[0][16])]
                      ]

    if(lista_acumulado[0][0] != None):
        lista_acumulado = [	['Colocación',  '$ {:0,.2f}'.format(lista_acumulado[0][0]), '%'],
                            ['Comisiones',  '$ {:0,.2f}'.format(
                                lista_acumulado[0][1]), '{:0,.2f}%'.format(lista_acumulado[0][9])],
                            ['Sueldos fijo',  '$ {:0,.2f}'.format(
                                lista_acumulado[0][2]), '{:0,.2f}%'.format(lista_acumulado[0][10])],
                            ['Carga social + aguinaldo',  '$ {:0,.2f}'.format(
                                lista_acumulado[0][3]), '{:0,.2f}%'.format(lista_acumulado[0][11])],
                            ['Viáticos',  '$ {:0,.2f}'.format(
                                lista_acumulado[0][4]), '{:0,.2f}%'.format(lista_acumulado[0][12])],
                            ['Gasolina',  '$ {:0,.2f}'.format(
                                lista_acumulado[0][5]), '{:0,.2f}%'.format(lista_acumulado[0][13])],
                            ['Costo autos',  '$ {:0,.2f}'.format(
                                lista_acumulado[0][6]), '{:0,.2f}%'.format(lista_acumulado[0][14])],
                            ['Rentas',  '$ {:0,.2f}'.format(
                                lista_acumulado[0][7]), '{:0,.2f}%'.format(lista_acumulado[0][15])],
                            ['TOTAL',  '$ {:0,.2f}'.format(
                                lista_acumulado[0][8]), '{:0,.2f}%'.format(lista_acumulado[0][16])]
                            ]

    lista_meses = [	'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul',
                    'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

    lista_costo = []

    temp01 = []
    temp02 = []

    for i in range(mes_numero):
        i += 1
        # SE GeNErA EL QUERY
        query03 = """select  sum(monto_dispuesto) as colocacion
        from BUO_Masnomina.contratos_hist 
        where 1 = 1 """
        if(i == 12):
            query03 += "and fecha_disposicion >= '" + \
                str(anio) + "-12-01' and fecha_disposicion < '" + \
                str(anio + 1) + "-01-01' "
        else:
            query03 += "and fecha_disposicion >= '" + str(anio) + "-" + formatear_no_mes(
                i) + "-01' and fecha_disposicion < '" + str(anio) + "-" + formatear_no_mes(i + 1) + "-01' "
        query03 += "and mes = " + str(anio) + formatear_no_mes(i) + " "
        if(int(division)):
            query03 += "and division = " + division + " "
        if(producto != "0"):
            query03 += "and producto = '" + producto + "' "
        
        query04 = """select
        sum(col.comisiones) + sum(col.sueldo_fijo) + sum(col.carga_social_aguinaldo) + sum(col.viaticos) + sum(col.gasolina) + sum(col.costos_autos) + sum(col.rentas)      
        from BUO_Masnomina.costo_colocacion_hist col
        where 1 = 1 """
        query04 += "and mes = " + str(anio) + formatear_no_mes(i) + " "
        if(int(division)):
            query04 += "and division = " + division + " "


        temp01.append(obtener_datos(query03, False, ()))
        temp02.append(obtener_datos(query04, False, ()))

    for i in range(len(temp01)):
        lista_costo.append([lista_meses[i] + ' ' + mes[0] + mes[1] +
                                mes[2] + mes[3], '{:0,.2f}'.format((temp02[i][0][0]*100)/temp01[i][0][0])])
    
    if(lista_costo):
        for i in range(12 - mes_numero):
            lista_costo.append([lista_meses[i + mes_numero] + ' ' + mes[0] + mes[1] +
                                mes[2] + mes[3], [0.0]])
    
    lista_resultado = {}

    if(lista_acumulado[0][0] != None):
        lista_resultado['nombre_mes'] = lista_meses[mes_numero - 1] + \
            ' ' + mes[0] + mes[1] + mes[2] + mes[3]
        lista_resultado['resultado_mes'] = lista_mes
        lista_resultado['resultado_acumulado'] = lista_acumulado
        lista_resultado['resultado_costo'] = lista_costo

    return json.dumps(lista_resultado)

"""


# tabla plantilla
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
    # si Rest.py
    app.run(host='127.0.0.1', debug=True, port=9999, threaded=DEBUG)

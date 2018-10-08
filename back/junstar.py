def main():
    lista_estados_supervisores =[
        [(201708, u'GUANAJUATO', 1), (201708, u'GUERRERO', 1), (201708, u'HIDALGO', 1), (201708, u'PUEBLA', 1), 
        (201709, u'GUANAJUATO', 1), (201709, u'GUERRERO', 1), (201709, u'HIDALGO', 1), (201709, u'PUEBLA', 1), 
        (201710, u'GUANAJUATO', 1), (201710, u'GUERRERO', 1), (201710, u'HIDALGO', 1), (201710, u'PUEBLA', 1), 
        (201711, u'GUANAJUATO', 1), (201711, u'GUERRERO', 2), (201711, u'HIDALGO', 1), (201711, u'PUEBLA', 1),
        (201712, u'GUANAJUATO', 1), (201712, u'GUERRERO', 2), (201712, u'HIDALGO', 1), (201712, u'PUEBLA', 1),
        (201801, u'GUANAJUATO', 1), (201801, u'GUERRERO', 3), (201801, u'HIDALGO', 1), (201801, u'PUEBLA', 2), (201801, u'QUERETARO', 1), 
        (201802, u'GUANAJUATO', 1), (201802, u'GUERRERO', 2), (201802, u'HIDALGO', 1), (201802, u'PUEBLA', 2),(201802, u'QUERETARO', 1), 
        (201803, u'GUANAJUATO', 1), (201803, u'GUERRERO', 3), (201803, u'HIDALGO', 1), (201803, u'MORELOS', 1), (201803, u'PUEBLA', 2), (201803, u'QUERETARO', 1), 
        (201804, u'GUANAJUATO', 1), (201804, u'GUERRERO', 1), (201804, u'HIDALGO', 1), (201804, u'PUEBLA', 2), (201805, u'GUANAJUATO', 1), (201805, u'GUERRERO', 1), (201805, u'HIDALGO', 1), (201805, u'PUEBLA', 2), 
        (201806, u'GUANAJUATO', 1), (201806, u'GUERRERO', 1), (201806, u'HIDALGO', 1), (201806, u'PUEBLA', 1), (201806, u'QUERETARO', 1),
        (201807, u'GUANAJUATO', 1), (201807, u'GUERRERO', 1), (201807, u'HIDALGO', 1), (201807, u'PUEBLA', 1), (201807, u'QUERETARO', 1), 
        (201808, u'GUANAJUATO', 1), (201808, u'HIDALGO', 1), (201808, u'PUEBLA', 1), (201808, u'QUERETARO', 1)]]
    
        
    mes = 8
    anio = 2018
    arregloFinal = []
    temp = lista_estados_supervisores.pop()

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
    
    print(arregloFinal)

def formatear_no_mes(mes):
    if(mes < 10):
        return '0' + str(mes)
    else:
        return str(mes)


if __name__ == '__main__':
    main()
lista_estados_supervisores = [
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
    (201808, u'GUANAJUATO', 1), (201808, u'HIDALGO', 1), (201808, u'PUEBLA', 1), (201808, u'QUERETARO', 1)]
]
    
    
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

print(arregloPromedio)
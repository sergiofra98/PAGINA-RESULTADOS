# # -*- coding: utf-8 -*-

def main():
        lista_mes = [(1656806.84, 171475.9263, 128329.74, 83601.73, 18707.28, 3208.8, 15839.0379, 11840.64, 433003.15419999993)]
        lista_acumulado = [(12605308.03, 1215582.4795, 886302.8700000001, 561628.79, 89084.04000000001, 22602.36, 90935.72739999999, 85208.34, 2951344.6069)]

        lista_mes = [	['Colocación',  '$ {:0,.2f}'.format(lista_mes[0][0]), '%'],
                      ['Comisiones',  '$ {:0,.2f}'.format(
                          lista_mes[0][1]), '{:0,.2f}%'.format((lista_mes[0][1]*100)/lista_mes[0][0])],
                      ['Sueldos fijo',  '$ {:0,.2f}'.format(
                          lista_mes[0][2]), '{:0,.2f}%'.format((lista_mes[0][2]*100)/lista_mes[0][0])],
                      ['Carga social + aguinaldo',  '$ {:0,.2f}'.format(
                          lista_mes[0][3]), '{:0,.2f}%'.format((lista_mes[0][3]*100)/lista_mes[0][0])],
                      ['Viáticos',  '$ {:0,.2f}'.format(
                          lista_mes[0][4]), '{:0,.2f}%'.format((lista_mes[0][4]*100)/lista_mes[0][0])],
                      ['Gasolina',  '$ {:0,.2f}'.format(
                          lista_mes[0][5]), '{:0,.2f}%'.format((lista_mes[0][5]*100)/lista_mes[0][0])],
                      ['Costo autos',  '$ {:0,.2f}'.format(
                          lista_mes[0][6]), '{:0,.2f}%'.format((lista_mes[0][6]*100)/lista_mes[0][0])],
                      ['Rentas',  '$ {:0,.2f}'.format(
                          lista_mes[0][7]), '{:0,.2f}%'.format((lista_mes[0][7]*100)/lista_mes[0][0])],
                      ['TOTAL',  '$ {:0,.2f}'.format(
                          lista_mes[0][8]), '{:0,.2f}%'.format((lista_mes[0][8]*100)/lista_mes[0][0])]
                      ]
        lista_acumulado = [	['Colocación',  '$ {:0,.2f}'.format(lista_acumulado[0][0]), '%'],
                            ['Comisiones',  '$ {:0,.2f}'.format(
                                lista_acumulado[0][1]), '{:0,.2f}%'.format((lista_acumulado[0][1]*100)/lista_acumulado[0][0])],
                            ['Sueldos fijo',  '$ {:0,.2f}'.format(
                                lista_acumulado[0][2]), '{:0,.2f}%'.format((lista_acumulado[0][2]*100)/lista_acumulado[0][0])],
                            ['Carga social + aguinaldo',  '$ {:0,.2f}'.format(
                                lista_acumulado[0][3]), '{:0,.2f}%'.format((lista_acumulado[0][3]*100)/lista_acumulado[0][0])],
                            ['Viáticos',  '$ {:0,.2f}'.format(
                                lista_acumulado[0][4]), '{:0,.2f}%'.format((lista_acumulado[0][4]*100)/lista_acumulado[0][0])],
                            ['Gasolina',  '$ {:0,.2f}'.format(
                                lista_acumulado[0][5]), '{:0,.2f}%'.format((lista_acumulado[0][5]*100)/lista_acumulado[0][0])],
                            ['Costo autos',  '$ {:0,.2f}'.format(
                                lista_acumulado[0][6]), '{:0,.2f}%'.format((lista_acumulado[0][6]*100)/lista_acumulado[0][0])],
                            ['Rentas',  '$ {:0,.2f}'.format(
                                lista_acumulado[0][7]), '{:0,.2f}%'.format((lista_acumulado[0][7]*100)/lista_acumulado[0][0])],
                            ['TOTAL',  '$ {:0,.2f}'.format(
                                lista_acumulado[0][8]), '{:0,.2f}%'.format((lista_acumulado[0][8]*100)/lista_acumulado[0][0])]
                            ]

        print(2)
if __name__ == '__main__':
    main()

var graficaColocacion = 0
var graficaEstado = 0
var graficaAsesor = 0
var graficaMNBrokers = 0

$(document).ready(function () {
    if (mes < 10) {
        $("#selectorFecha").append("<b>01-" + (ano - 1) + "</b> a <b>0" + mes + "-" + ano + "</b>");
    }
    else {
        $("#selectorFecha").append("<b>01-" + (ano - 1) + "</b> a <b>" + mes + "-" + ano + "</b>");
    }
});

function getColocacion() {
    $(".tablasHead").html("");
    $("#tablaColocacionBody").html("");
    $("#tablaAsesorPromBody").html("");
    $("#tablaBrokersBody").html("");
    $("#tablaAsesorBody").html("");
    $("#tablaSupervisorPromBody").html("");
    $("#tablaSupervisorBody").html("");

    if (graficaColocacion)
        graficaColocacion.destroy()
    if (graficaEstado)
        graficaEstado.destroy()
    if (graficaAsesor)
        graficaAsesor.destroy()
    if (graficaMNBrokers)
        graficaMNBrokers.destroy()

    $('#landing').css("display", "none");
    $('#loading').css("display", "flex");
    $('.cuerpo, #titulo').css("display", "none");

    $.getJSON(linkREST + "consulta_estado_colocacion", {
        mes: $('#inputFecha').val(),
        division: $('#inputDivision').val(),
        producto: $('#inputProducto').val()
    },
        function (dataTablas) {
            console.log(dataTablas)
            if (jQuery.isEmptyObject(dataTablas)) {
                $("#alertaNoResultados").css('display', 'block')
                $('#loading').css("display", "none");
                $('#landing').css("display", "flex");
                $('.cuerpo, #titulo').css("display", "none");
                return;
            }

            let i = 0;
            let j = 0;
            let append = '<th></th>'
            for (i; i < 13; i++) {
                append += '<th>' + dataTablas.meses[i] + '</th>';
            }
            append += '<th><b>Total Año</b></th><th><b>Total AA</b></th> <th><b>Total</b></th>'

            $(".tablasHead").append(append);

            //SE PEGAN LAS TABLAS DE ESTADOS
            append = ''
            for (i = 0; i < dataTablas.estados.length; i++) {
                append += '<tr>'
                for(j = 0; j < 17; j++){
                    append += '<th>' + dataTablas.estados[i][j] + '</th>';
                }
                append += '</tr>'
            }

            $("#tablaColocacionBody").append(append);

            //SE PEGAN LAS TABLAS DE SUPERVISORES
            append = ''
            for (i = 0; i < dataTablas.lista_supervisores.length; i++) {
                append += '<tr>'
                for(j = 0; j < 17; j++){
                    append += '<th>' + dataTablas.lista_supervisores[i][j] + '</th>';
                }
                append += '</tr>'
            }

            $("#tablaSupervisorBody").append(append);

            //SE PEGAN LAS TABLAS DE ASESORES
            append = ''
            for (i = 0; i < dataTablas.lista_asesores.length; i++) {
                append += '<tr>'
                for(j = 0; j < 17; j++){
                    append += '<th>' + dataTablas.lista_asesores[i][j] + '</th>';
                }
                append += '</tr>'
            }

            $("#tablaAsesorBody").append(append);

            //SE PEGAN LAS TABLAS DE PROMEDIO DE ASESOR
            append = ''
            for (i = 0; i < dataTablas.lista_asesores_promedio.length; i++) {
                append += '<tr>'
                for(j = 0; j < 17; j++){
                    append += '<th>' + dataTablas.lista_asesores_promedio[i][j] + '</th>';
                }
                append += '</tr>'
            }

            $("#tablaAsesorPromBody").append(append);

            //SE PEGAN LAS TABLAS DE PROMEDIO DE SUPERVISOR
            append = ''
            for (i = 0; i < dataTablas.lista_supervisores_promedio.length; i++) {
                append += '<tr>'
                for(j = 0; j < 17; j++){
                    append += '<th>' + dataTablas.lista_supervisores_promedio[i][j] + '</th>';
                }
                append += '</tr>'
            }

            $("#tablaSupervisorPromBody").append(append);


            /*totalAno = dataTablas.estados.pop().valores;

            function esteAno() {
                temp = []
                for (const prep in totalAno) {
                    if (prep < 13) {
                        temp.push(parseInt((`${totalAno[prep]}`).replace(/,/g, '')));

                    }
                }
                return temp
            }

            function pasadoAno() {
                temp = []
                for (const prep in totalAno) {
                    if (prep > 12) {
                        temp.push(parseInt((`${totalAno[prep]}`).replace(/,/g, '')));
                    }
                }
                return temp;
            }

            function estadoGenerador() {
                temp = [];

                for (i = 0; i < dataTablas.estados.length; i++) {
                    temp2 = [];
                    for (const prep in dataTablas.estados[i].valores) {
                        if (prep > 12) {
                            temp2.push(parseInt((`${dataTablas.estados[i].valores[prep]}`).replace(/,/g, '')))
                        }
                    }
                    temp.push({
                        data: temp2,
                        label: dataTablas.estados[i].nombre,
                        borderColor: generadorColoresUno(i),
                        backgroundColor: generadorColoresUno(i),
                        fill: false
                    });
                }
                return temp;
            }

            function generadorPromedio() {
                temp = [];
                promedio = dataTablas.promedios_asesor.pop()
                for (const prep in promedio.valores) {
                    temp.push(parseInt((`${promedio.valores[prep]}`).replace(/,/g, '')));
                }
                return temp;
            }

            function generadorMNvsBrokers() {
                temp = [];
                temp2 = [];
                temp3 = [];
                total = dataTablas.brokers.pop();

                for (const prep in total.valores) {
                    if (prep > 12) {
                        temp.push(parseInt((`${total.valores[prep]}`).replace(/,/g, '')));
                    }
                }


                for (const prep in dataTablas.total_general.valores) {
                    if (prep > 12) {
                        temp2.push(parseInt((`${dataTablas.total_general.valores[prep]}`).replace(/,/g, '')));
                    }
                }

                for (let i = 0; i < temp.length; i++) {
                    temp[i] = (temp[i] * 100 / temp2[i]).toFixed(2);
                    temp3.push(100 - temp[i])
                }

                return [temp, temp3]
            }

            arregloMNN = generadorMNvsBrokers()

            declararCharts(
                {
                    labels: ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC'],
                    datasets: [
                        {
                            data: esteAno(),
                            label: ano - 1,
                            borderColor: "#cc0d0d",
                            backgroundColor: "#cc0d0d",
                            fill: false
                        }, {
                            data: pasadoAno(),
                            label: ano,
                            borderColor: "#3e95cd",
                            backgroundColor: "#3e95cd",
                            fill: false
                        }
                    ]
                },
                {
                    labels: ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC'],
                    datasets: estadoGenerador()
                },
                {
                    labels: dataTablas.meses,
                    datasets: [{
                        data: generadorPromedio(),
                        borderColor: "#007bff",
                        backgroundColor: "#007bff",
                        label: "Ventas de asesores por mes",
                        fill: false
                    }]
                },
                {
                    labels: ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC'],
                    datasets: [
                        {
                            data: arregloMNN[1],
                            borderColor: "#3e95cd",
                            backgroundColor: "#3e95cd",
                            fill: false,
                            label: "Asesores MN"
                        },
                        {
                            data: arregloMNN[0],
                            borderColor: "#cc0d0d",
                            backgroundColor: "#cc0d0d",
                            fill: false,
                            label: "Brookers"
                        }
                    ]
                }
            )*/

        })
        .done(function () {
            $('#body, #titulo').css("display", "flex");
            $('.cuerpo').css('display', 'block')
            $('#loading').css("display", "none");
        })
        .fail(function (textStatus) {
            $('#loading').css("display", "none");
            $('#landing').css("display", "flex");
            $("#alertaConsulta").css('display', 'block');
        });
}

function declararCharts(data1, data2, data3, data4) {
    graficaColocacion = new Chart($("#canvasGraficaColocacion"), {
        type: 'line',
        data: data1,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Colocación',
                fontSize: 16
            },
            legend: {
                position: "bottom"
            },
            tooltips: {
                mode: 'label',
                label: 'mylabel',
                callbacks: {
                    label: function (tooltipItem, data) {
                        return '$' + tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                    },
                }
            },
            scales: {
                yAxes: [
                    {
                        ticks: {
                            callback: function (label, index, labels) {
                                return label / 1000000 + 'm';
                            }
                        },
                        scaleLabel: {
                            display: true,
                            labelString: '1m = 1,000,000'
                        }
                    }
                ]
            }
        }
    });
    graficaEstado = new Chart($("#canvasGraficaEstado"), {
        type: 'line',
        data: data2,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Colocación por estado',
                fontSize: 16
            },
            legend: {
                position: "bottom"
            },
            tooltips: {
                mode: 'label',
                label: 'mylabel',
                callbacks: {
                    label: function (tooltipItem, data) {
                        return '$' + tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                    },
                }
            },
            scales: {
                yAxes: [
                    {
                        ticks: {
                            callback: function (label) {
                                return (label / 1000).toLocaleString() + 'k';
                            }
                        },
                        scaleLabel: {
                            display: true,
                            labelString: '1k = 1,000'
                        }
                    }
                ]
            }
        }
    });
    graficaAsesor = new Chart($("#canvasGraficaAsesor"), {
        type: 'line',
        data: data3,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Colocación Promedio de Asesor',
                fontSize: 16
            },
            legend: {
                display: false
            },
            tooltips: {
                mode: 'label',
                label: 'mylabel',
                callbacks: {
                    label: function (tooltipItem, data) {
                        return '$' + tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                    },
                }
            },
            scales: {
                yAxes: [
                    {
                        ticks: {
                            callback: function (label) {
                                return (label / 1000).toLocaleString() + 'k';
                            }
                        },
                        scaleLabel: {
                            display: true,
                            labelString: '1k = 1,000'
                        }
                    }
                ]
            }
        }
    });
    graficaMNBrokers = new Chart($("#canvasGraficaMNBrokers"), {
        type: 'bar',
        data: data4,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales:
            {
                xAxes: [{
                    stacked: true
                }],
                yAxes: [{
                    ticks: {
                        callback: function (label) {
                            return label + '%';
                        }
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Porcentaje'
                    }
                }]
            },
            title: {
                display: true,
                text: 'MN vs Brokers',
                fontSize: 16
            },
            legend: {
                position: "bottom"
            },
            tooltips: {
                mode: 'label',
                label: 'mylabel',
                callbacks: {
                    label: function (tooltipItem, data) {
                        return tooltipItem.yLabel + '%';
                    },
                }
            }
        }
    });
}
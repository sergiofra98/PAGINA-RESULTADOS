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
    $("#tablaColocacionHead").html("");
    $("#tablaBrokersHead").html("");
    $("#tablaColocacionBody").html("");
    $("#tablaAsesorHead").html("");
    $("#tablaAsesorPromHead").html("");
    $("#tablaAsesorPromBody").html("");
    $("#tablaBrokersBody").html("");
    $("#tablaAsesorBody").html("");
    $("#tablaSupervisorPromBody").html("");
    $("#tablaSupervisorBody").html("");
    $(".tablaAsesorHead").html("");

    if (graficaColocacion)
        graficaColocacion.destroy()
    if (graficaEstado)
        graficaEstado.destroy()
    if (graficaAsesor)
        graficaAsesor.destroy()
    if (graficaMNBrokers)
        graficaMNBrokers.destroy()

    $('#body, #titulo').hide();
    $('#landing').css("display", "none");
    $('#loading').css("display", "flex");

    $.getJSON(linkREST + "consulta_estado_colocacion", {
        mes: $('#inputAno').val() + $('#inputMes').val(),
        division: $('#inputDivision').val(),
        producto: $('#inputProducto').val()
    },
        function (dataTablas) {
            if (!dataTablas) {
                $("#alertaNoResultados").css('display', 'block')
                return;
            }
            var append = '<th></th>'
            for (const prop in dataTablas.meses) {
                append += '<th>' + (`${dataTablas.meses[prop]}`) + '</th>';
            }
            append += '<th>Total ' + ano + ' </th> <th>Promedio</th>'

            $("#tablaColocacionHead").append(append);

            append = "";
            for (let i = 0; i < dataTablas.estados.length; i++) {

                if (i === dataTablas.estados.length - 1) {
                    append += '<tr class="obscuro texto"><td>' + dataTablas.estados[i].nombre + '</td>';
                }
                else {
                    append += '<tr><td class="texto">' + dataTablas.estados[i].nombre + "</td>";
                }


                for (const prop in dataTablas.estados[i].valores) {
                    append += '<td class="numero">' + (`${dataTablas.estados[i].valores[prop]}`) + '</td>'
                }
                append += '<td class="obscuro numero">' + dataTablas.estados[i].suma_anio + '</td>'
                append += '<td class="numero">' + dataTablas.estados[i].promedio_anio + '</td>'

                append += "</tr>"
            }

            append += '<tr><td  class="texto">BROKERS</td>'
            let totalBrokers = dataTablas.brokers.length - 1;

            for (const prop in dataTablas.brokers[totalBrokers].valores) {
                append += '<td class="numero">' + (`${dataTablas.brokers[totalBrokers].valores[prop]}`) + '</td>'
            }
            append += '<td class="obscuro numero">' + dataTablas.brokers[totalBrokers].suma_anio + '</td><td>' +
                dataTablas.brokers[totalBrokers].promedio_anio + '</td></tr><tr class="texto obscuro"><td>TOTAL GENERAL</td>'

            for (const prop in dataTablas.total_general.valores) {
                append += '<td class="numero">' + (`${dataTablas.total_general.valores[prop]}`) + '</td>'
            }
            append += '<td class="numero">' + dataTablas.total_general.suma_anio + '</td><td>' + dataTablas.total_general.promedio_anio + '</td></tr>'

            $("#tablaColocacionBody").append(append);

            //PEGAR TABLA DE BROKERS
            // append = "";

            // for (let i = 0; i < dataTablas.brokers.length; i++) {

            //     if (i === dataTablas.brokers.length - 1) {
            //         append += '<tr class="obscuro texto"><td>' + dataTablas.brokers[i].nombre.replace(/_/g, ' '); + '</td>';
            //     }
            //     else {
            //         append += '<tr><td class="texto">' + dataTablas.brokers[i].nombre.replace(/_/g, ' '); + "</td>";
            //     }


            //     for (const prop in dataTablas.brokers[i].valores) {
            //         append += '<td class="numero">' + (`${dataTablas.brokers[i].valores[prop]}`) + '</td>'
            //     }
            //     append += '<td class="obscuro numero">' + dataTablas.brokers[i].suma_anio + '</td><td>' + dataTablas.brokers[i].promedio_anio + '</td></tr>'
            // }

            // $("#tablaBrokersBody").append(append);

            //PEGAR TABLA DE ASESOR PROMEDIOS
            append = '<th></th>'
            for (const prop in dataTablas.meses) {
                append += '<th>' + (`${dataTablas.meses[prop]}`) + '</th>';
            }
            $(".tablaAsesorHead").append(append);

            append = "";
            for (let i = 0; i < dataTablas.promedios_asesor.length; i++) {

                if (i === dataTablas.promedios_asesor.length - 1) {
                    append += '<tr class="obscuro"><td class="texto">' + dataTablas.promedios_asesor[i].nombre.replace(/_/g, ' '); + '</td>';
                }
                else {
                    append += '<tr><td class="texto">' + dataTablas.promedios_asesor[i].nombre.replace(/_/g, ' '); + "</td>";
                }


                for (const prep in dataTablas.promedios_asesor[i].valores) {
                    append += '<td class="' + (`${dataTablas.promedios_asesor[i].valores[prep][1]}`) + ' numero">' + (`${dataTablas.promedios_asesor[i].valores[prep][0]}`) + '</td>'
                }

                append += "</tr>"
            }

            $("#tablaAsesorPromBody").append(append);

            //PEGAR TABLA DE ASESOR 
            append = "";
            for (let i = 0; i < dataTablas.asesores.length; i++) {

                if (i === dataTablas.asesores.length - 1) {
                    append += '<tr class="obscuro texto"><td>' + dataTablas.asesores[i].nombre.replace(/_/g, ' '); + '</td>';
                }
                else {
                    append += '<tr><td class="texto">' + dataTablas.asesores[i].nombre.replace(/_/g, ' '); + "</td>";
                }


                for (const prep in dataTablas.asesores[i].valores) {
                    append += '<td class="numero">' + (`${dataTablas.asesores[i].valores[prep]}`) + '</td>'
                }
                append += "</tr>"
            }

            $("#tablaAsesorBody").append(append);

            //PEGAR TABLA DE SUPEERVISORES PROMEDIOS
            append = "";
            for (let i = 0; i < dataTablas.promedios_asesor.length; i++) {

                if (i === dataTablas.promedios_asesor.length - 1) {
                    append += '<tr class="obscuro"><td class="texto">' + dataTablas.promedios_asesor[i].nombre.replace(/_/g, ' '); + '</td>';
                }
                else {
                    append += '<tr><td class="texto">' + dataTablas.promedios_asesor[i].nombre.replace(/_/g, ' '); + "</td>";
                }


                for (const prep in dataTablas.promedios_asesor[i].valores) {
                    append += '<td class="' + (`${dataTablas.promedios_asesor[i].valores[prep][1]}`) + ' numero">' + (`${dataTablas.promedios_asesor[i].valores[prep][0]}`) + '</td>'
                }

                append += "</tr>"
            }

            $("#tablaSupervisorPromBody").append(append);

            //PEGAR TABLA DE SUPEERVISORES 
            append = "";
            for (let i = 0; i < dataTablas.asesores.length; i++) {

                if (i === dataTablas.asesores.length - 1) {
                    append += '<tr class="obscuro texto"><td>' + dataTablas.asesores[i].nombre.replace(/_/g, ' '); + '</td>';
                }
                else {
                    append += '<tr><td class="texto">' + dataTablas.asesores[i].nombre.replace(/_/g, ' '); + "</td>";
                }


                for (const prep in dataTablas.asesores[i].valores) {
                    append += '<td class="numero">' + (`${dataTablas.asesores[i].valores[prep]}`) + '</td>'
                }
                append += "</tr>"
            }

            $("#tablaSupervisorBody").append(append);



            totalAno = dataTablas.estados.pop().valores;

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
            )

        })
        .done(function () {
            $('#body, #titulo').css("display", "flex");
            $('#loading').css("display", "none");
        })
        .fail(function (textStatus) {
            $('#loading').css("display", "none");
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
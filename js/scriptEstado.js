var graficaColocacion = 0
var graficaEstado = 0
var graficaAsesor = 0
var graficaMNBrokers = 0

$(document).ready(function () {
    if (mes < 10) {
        $("#selectorFecha").append("Periodo:  <b>01-" + (ano - 1) + "</b> a <b>0" + mes + "-" + ano + "</b>");
    }
    else {
        $("#selectorFecha").append("Periodo:  <b>01-" + (ano - 1) + "</b> a <b>" + mes + "-" + ano + "</b>");
    }
});

function getEstado() {
    $("#tablaColocacionHead").html("");
    $("#tablaBrokersHead").html("");
    $("#tablaColocacionBody").html("");
    $("#tablaAsesorHead").html("");
    $("#tablaAsesorPromHead").html("");
    $("#tablaAsesorPromBody").html("");
    $("#tablaBrokersBody").html("");
    $("#tablaAsesorBody").html("");

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

    $.getJSON(linkREST + "consulta_estado_colocacion", {},
        function (dataTablas) {
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
                dataTablas.brokers[totalBrokers].promedio_anio + '</td></tr><tr class="obscuro"><td>TOTAL GENERAL</td>'

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
            $("#tablaAsesorHead").append(append);

            append = "";
            for (let i = 0; i < dataTablas.promedios.length; i++) {

                if (i === dataTablas.promedios.length - 1) {
                    append += '<tr class="obscuro texto"><td>' + dataTablas.promedios[i].nombre.replace(/_/g, ' '); + '</td>';
                }
                else {
                    append += '<tr><td class="texto">' + dataTablas.promedios[i].nombre.replace(/_/g, ' '); + "</td>";
                }


                for (const prep in dataTablas.promedios[i].valores) {
                    append += '<td class="' + (`${dataTablas.promedios[i].valores[prep][1]}`) + ' numero">' + (`${dataTablas.promedios[i].valores[prep][0]}`) + '</td>'
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
                        borderColor: generadorColores(1),
                        backgroundColor: generadorColores(1),
                        fill: false
                    });
                }
                return temp;
            }

            function generadorPromedio() {
                temp = [];
                promedio = dataTablas.promedios.pop()
                for (const prep in promedio.valores) {
                    temp.push(parseInt((`${promedio.valores[prep]}`).replace(/,/g, '')));
                }
                return temp;
            }

            function generadorMNvsBrokers() {
                temp = [];
                temp2 = [];
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
                }
                return temp
            }

            declararCharts(
                {
                    labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
                    datasets: [{
                        data: esteAno(),
                        label: ano,
                        borderColor: "#3e95cd",
                        backgroundColor: "#3e95cd",
                        fill: false
                    }, {
                        data: pasadoAno(),
                        label: ano - 1,
                        borderColor: "#8e5ea2",
                        backgroundColor: "#8e5ea2",
                        fill: false
                    }]
                },
                {
                    labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
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
                    labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
                    datasets: [{
                        data: generadorMNvsBrokers(),
                        borderColor: "#007bff",
                        backgroundColor: "#007bff",
                        fill: false,
                        label: "Porcentaje de contribución de brokers"
                    }]
                }
            )

        })
        .done(function () {
            $('#body, #titulo').css("display", "flex");
            $('#loading').css("display", "none");
        })
        .fail(function (textStatus) {
            $('#loading').css("display", "none");
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
                text: 'Colocación'
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
                text: 'Colocación por estado'
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
                text: 'Colocación Promedio de Asesor'
            },
            legend: { display: false }
        }
    });
    graficaMNBrokers = new Chart($("#canvasGraficaMNBrokers"), {
        type: 'bar',
        data: data4,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                xAxes: [{
                    stacked: true
                }],
                yAxes: [{
                    stacked: true
                }]
            },
            title: {
                display: true,
                text: 'MN vs Brokers'
            },
            legend: { display: false }
        }
    });
}
var graficaEstado = 0


function getColocacion() {
    $("#tablaMesHead").html("")
    $("#tablaMesBody").html("")
    $("#tablaAcumuladoBody").html("")
    $("#tablaCostoBody").html("")

    if (graficaEstado)
        graficaEstado.destroy()

    $('#body, #titulo').hide();
    $('#landing').css("display", "none");
    $('#loading').css("display", "flex");

    $.getJSON(linkREST + "costos_colocacion", {},
        function (dataTablas) {
            var i = 0;
            append = getStringMes(mes);
            console.log(dataTablas);

            $("#tablaMesHead").append('<th colspan="3">' + append + " " + ano + "</th>");

            append = "";

            append += '<tr style="border-bottom: 12px solid #9ba5af"><td class="texto">' + dataTablas.mes[0].nombre + '</td><td class="numero">$ ' + dataTablas.mes[0].valor + '</td><td style="text-align:center;">' + dataTablas.mes[0].porcentaje + '</td></tr>';

            for (i = 1; i < dataTablas.mes.length; i++) {
                if (i === dataTablas.mes.length - 1) {
                    append += '<tr class="obscuro"><td class="texto">' + dataTablas.mes[i].nombre + '</td><td class="numero">$ ' + dataTablas.mes[i].valor + "</td><td>" + dataTablas.mes[i].porcentaje + "</td></tr>";
                }
                else {
                    append += '<tr><td class="texto">' + dataTablas.mes[i].nombre + '</td><td class="numero">$ ' + dataTablas.mes[i].valor + "</td><td>" + dataTablas.mes[i].porcentaje + "</td></tr>";
                }
            }

            $("#tablaMesBody").append(append);

            append = "";

            append += '<tr style="border-bottom: 12px solid #9ba5af"><td class="texto">' + dataTablas.acumulado[0].nombre + '</td><td class="numero">$ ' + dataTablas.acumulado[0].valor + '</td><td style="text-align:center;">' + dataTablas.acumulado[0].porcentaje + '</td></tr>';

            for (i = 1; i < dataTablas.acumulado.length; i++) {
                if (i === dataTablas.acumulado.length - 1) {
                    append += '<tr class="obscuro"><td class="texto">' + dataTablas.acumulado[i].nombre + '</td><td class="numero">$ ' + dataTablas.acumulado[i].valor + "</td><td>" + dataTablas.acumulado[i].porcentaje + "</td></tr>";
                }
                else {
                    append += '<tr><td class="texto">' + dataTablas.acumulado[i].nombre + '</td><td class="numero">$ ' + dataTablas.acumulado[i].valor + "</td><td>" + dataTablas.acumulado[i].porcentaje + "</td></tr>";
                }
            }

            $("#tablaAcumuladoBody").append(append);

            append = "";

            for (i = 0; i < dataTablas.costo.length; i++) {
                if (i === dataTablas.costo.length - 1) {
                    append += '<tr class="obscuro"><td style="width = 100px;" class="texto">' + dataTablas.costo[i].nombre + '</td><td style="width = 100px;">' + dataTablas.costo[i].porcentaje + "</td></tr>";
                }
                else {
                    append += '<tr><td style="width = 100px;" class="texto">' + dataTablas.costo[i].nombre + ' </td><td style="width = 100px;">' + dataTablas.costo[i].porcentaje + "</td></tr>";
                }
            }

            $("#tablaCostoBody").append(append);

            function getdatos() {
                temp = [];
                let num;

                dataTablas.costo.forEach(element => {
                    num = parseFloat(element.porcentaje.replace(/%/g, ''));

                    if (num) {
                        temp.push(num);
                    }
                });

                temp.pop();

                return temp;
            }

            generarGraficas(
                {
                    labels: ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC'],
                    datasets: [{
                        data: getdatos(),
                        label: ano,
                        borderColor: "#3e95cd",
                        backgroundColor: "#3e95cd50",
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

function generarGraficas(data) {
    graficaEstado = new Chart($("#canvasCosto"), {
        type: 'line',
        data: data,
        options: {
            title: {
                display: true,
                text: 'Colocación por estado',
                fontSize: 22
            },
            legend: { display: false },
            elements: {
                line: {
                    tension: 0, // disables bezier curves
                }
            },
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

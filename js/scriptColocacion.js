var graficaEstado = 0


function getColocacion() {
    $("#tablaMesHead").html("")
    $("#tablaMesBody").html("")
    $("#tablaAcumuladoBody").html("")
    $("#tablaCostoBody").html("")

    if (graficaEstado)
        graficaEstado.destroy()

    $('#body, #titulo').hide();
    $('.cuerpo').css("display", "none");

    $('#landing').css("display", "none");
    $('#loading').css("display", "flex");

    $.getJSON(linkREST + "costos_colocacion", {
        mes: $('#inputAno').val() + '' + $('#inputMes').val(),
        division: $('#inputDivision').val(),
        producto: $('#inputProducto').val()
    },
        function (dataTablas) {
            if (jQuery.isEmptyObject(dataTablas)) {
                $("#alertaNoResultados").css('display', 'block')
                $('#loading').css("display", "none");
                $('#landing').css("display", "flex");

                $('.cuerpo, #titulo').css("display", "none");
                return;
            }
            else {
                console.log(dataTablas)
                var i = 0;
                var j = 0;
                append = getStringMes(mes);

                $("#tablaMesHead").append('<th colspan="3">' + dataTablas.nombre_mes + "</th>");

                append = "";
                append += '<tr style="border-bottom: 12px solid #9ba5af"><td class="texto">' + dataTablas.resultado_mes[0][0] + '</td><td class="numero">' + dataTablas.resultado_mes[0][1] + '</td><td style="text-align:center;">' + dataTablas.resultado_mes[0][2] + '</td></tr>';

                for (i = 1; i < 9; i++) {
                    append += "<tr>";

                    for (j = 0; j < 3; j++) {
                        append += "<td>" + dataTablas.resultado_mes[i][j] + "</td>";
                    }
                    append += "</tr>";

                }

                $("#tablaMesBody").append(append);

                append = "";
                append += '<tr style="border-bottom: 12px solid #9ba5af"><td class="texto">' + dataTablas.resultado_acumulado[0][0] + '</td><td class="numero">' + dataTablas.resultado_acumulado[0][1] + '</td><td style="text-align:center;">' + dataTablas.resultado_acumulado[0][2] + '</td></tr>';

                for (i = 1; i < 9; i++) {
                    append += "<tr>";

                    for (j = 0; j < 3; j++) {
                        append += "<td>" + dataTablas.resultado_acumulado[i][j] + "</td>";
                    }
                    append += "</tr>";

                }

                $("#tablaAcumuladoBody").append(append);

                append = "";

                for (i = 0; i < 12; i++) {
                    append += "<tr>"
                    for (j = 0; j < 2; j++) {
                        if (j == 1) {
                            append += '<td>' + dataTablas.resultado_costo[i][j] + "%</td>";
                        }
                        else {
                            append += '<td>' + dataTablas.resultado_costo[i][j] + "</td>";
                        }
                    }
                    append += "</tr>"
                }

                $("#tablaCostoBody").append(append);

                function getdatos() {
                    temp = [];

                    dataTablas.resultado_costo.forEach(element => {
                        if (element[1] != 0) {
                            temp.push(element[1]);
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

                $('#body, #titulo').css("display", "flex");
                $('.cuerpo').css("display", "flex");
            }
        })
        .done(function () {
            $('#loading').css("display", "none");
        })
        .fail(function (textStatus) {
            $('#loading').css("display", "none");
            $("#alertaConsulta").css('display', 'block');
            console.log(textStatus)
        })
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
            scales:
            {
                xAxes: [{
                    stacked: true
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        callback: function (label) {
                            return label + '%';
                        }
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Porcentaje'
                    }
                }]
            }
        }
    });
}

var graficaColocacion = 0;

function getColocacion() {
    $("#tablaColocacion").html("");
    $("#tablaCarteraMesA").html("");
    $("#tablaCarteraHeader").html("");
    $("#tablaCarteraAnoA").html("");

    if (graficaColocacion)
        graficaColocacion.destroy();


    $('#body, #titulo, #cartera').hide();
    $('#landing').css("display", "none");
    $('#loading').css("display", "flex");

    $.getJSON(linkREST + "consulta_convenio_colocacion",
        {
            mes: $('#inputAno').val() + $('#inputMes').val(),
            division: $('#inputDivision').val(),
            producto: $('#inputProducto').val()
        },
        function (dataTablas) {
            if (!dataTablas) {
                $("#alertaNoResultados").css('display', 'block')
                return;
            }
            append = "";

            for (let i = 0; i < dataTablas.length; i++) {
                append += '<tr>' +
                    '<td  class="texto">' + dataTablas[i].nombre + '</td>' +
                    '<td class="numero"> ' + dataTablas[i].total_mes + '</td>' +
                    '<td class="colObscuro">' + dataTablas[i].total_mes_pct + '</td>' +
                    '<td class="numero"> ' + dataTablas[i].total_mes_aa + '</td>' +
                    '<td class="colObscuro">' + dataTablas[i].total_mes_aa_pct + '</td>' +
                    '<td class="numero">' + dataTablas[i].total_acu_aa + '</td>' +
                    '<td class="numero">' + dataTablas[i].total_acu + '</td>' +
                    '<td class="colObscuro ' + dataTablas[i].color_acu + '">' + dataTablas[i].total_acu_comp_pct + '</td>' +
                    '</tr>';
            }

            $("#tablaColocacion").append(append);

            dataTablas.pop();

            generarGraficas(
                dataTablas.map(a => a.nombre),
                dataTablas.map(a => parseInt(a.total_mes.replace(/,/g, ''))),
                generadorColores(dataTablas.length)
            )
        }
    )
        .done(function () {
            $('#body, #titulo, #cartera').css("display", "flex");
            $('#loading').css("display", "none");
        })
        .fail(function (textStatus) {
            $('#loading').css("display", "none");
            $("#alertaConsulta").css('display', 'block')
        });

    $.getJSON(linkREST + "consulta_convenio_cartera",
        {
            division: $("#inputDivision").val(),
            mes: $('#inputAno').val() + $('#inputMes').val()
        },
        function (dataTablas) {
            let i = 0;
            append = '<th><div style = "width: 168px;display:block;"></div ></th >' +
                '<th colspan="1">' + dataTablas.meses[1] + '</th>' +
                '<th colspan="1">' + dataTablas.meses[2] + '</th>' +
                '<th colspan="2" style="border-right:#535353 solid 2px;">VS MA</th>' +
                '<th colspan="1">' + dataTablas.meses[0] + '</th>' +
                '<th colspan="1">' + dataTablas.meses[2] + '</th>' +
                '<th colspan="2">VS MAA</th>';

            $("#tablaCarteraHeader").append(append);


            append = "";
            for (i = 0; i < dataTablas.cartera.length; i++) {
                append += '<tr >' +
                    '<td  class="texto">' + dataTablas.cartera[i].nombre + '</td>' +
                    '<td class="numero"> ' + dataTablas.cartera[i].total_ma + '</td>' +
                    '<td class="colObscuro numero"> ' + dataTablas.cartera[i].total_mes + '</td>' +
                    '<td class="numero"> ' + dataTablas.cartera[i].total_mes_vs_ma + '</td>' +
                    '<td class="colObscuro ' + dataTablas.cartera[i].colorMA + '" style="border-right:#535353 solid 2px;">' + dataTablas.cartera[i].total_mes_vs_ma_pct + '</td>' +
                    '<td class="numero"> ' + dataTablas.cartera[i].total_mes + '</td>' +
                    '<td class="colObscuro numero"> ' + dataTablas.cartera[i].total_maa + '</td>' +
                    '<td  class="numero"> ' + dataTablas.cartera[i].total_mes_vs_maa + '</td>' +
                    '<td class="colObscuro ' + dataTablas.cartera[i].colorMAA + '">' + dataTablas.cartera[i].total_mes_vs_maa_pct + '</td>' +
                    '</tr>';

            }

            $("#tablaCarteraMesA").append(append);
        })
        .done(function () {
            $('#body, #titulo, #cartera').css("display", "flex");
            $('#loading').css("display", "none");
        })
        .fail(function (textStatus) {
            $('#loading').css("display", "none");
            $("#alertaConsulta").css('display', 'block')
        });
}

function generarGraficas(labels, data, colors) {
    graficaColocacion = new Chart($("#canvasGraficaColocacion"), {
        type: 'bar',
        options: {
            title: {
                display: true,
                position: "top",
                text: "Colocación del Mes",
                fontSize: 24,
                fontColor: "#111"
            },
            responsive: true,
            maintainAspectRatio: false,
            legend: { display: false },
            tooltips: {
                callbacks: {
                    label: function (tooltipItem, data) {
                        //get the concerned dataset
                        var dataset = data.datasets[tooltipItem.datasetIndex];
                        //calculate the total of this data set
                        var total = dataset.data.reduce(function (previousValue, currentValue, currentIndex, array) {
                            return previousValue + currentValue;
                        });
                        //get the current items value
                        var currentValue = dataset.data[tooltipItem.index];
                        //calculate the precentage based on the total and current item, also this does a rough rounding to give a whole number
                        var precentage = Math.floor((currentValue / total) * 100);
                        return labels[tooltipItem.index] + ": " + precentage + "%";
                    }
                }
            },
            scales:
            {
                xAxes: [{
                    stacked: true,
                    ticks: {
                        autoSkip: false
                    }
                }],
                yAxes: [{
                    ticks: {
                        callback: function (label) {
                            return (label / 1000).toLocaleString() + 'k';
                        }
                    },
                    scaleLabel: {
                        display: true,
                        labelString: '1k = 1,000'
                    }
                }]
            }
        },
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors,
            }]
        }
    });
}


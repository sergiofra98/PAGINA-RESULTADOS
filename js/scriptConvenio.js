var graficaColocacion = 0;

function getColocacion() {
    $("#tablaColocacion").html("");
    $("#tablaCarteraMesA").html("");
    $("#tablaCarteraAnoA").html("");

    if(graficaColocacion)
        graficaColocacion.destroy();
    

    $('#body, #titulo, #cartera').hide();
    $('#landing').css("display", "none");
    $('#loading').css("display", "flex");

    $.getJSON(linkREST + "consulta_convenio_colocacion",
        {
            division: $("#inputDivision").val(),
            mes: $("#inputMes").val(),
        },
        function (dataTablas) {
            dataTablas.forEach(function (i) {
                $("#tablaColocacion").append('<tr>' +
                    '<td>' + i.nombre + '</td>' +
                    '<td>' + i.total_mes + '</td>' +
                    '<td class="colObscuro">' + i.total_mes_pct + '</td>' +
                    '<td>' + i.total_mes_aa + '</td>' +
                    '<td class="colObscuro">' + i.total_mes_aa_pct + '</td>' +
                    '</tr>');
            });
            dataTablas.pop()
        })
        .done(function () {
            $('#body, #titulo, #cartera').css("display", "flex");
            $('#loading').css("display", "none");
        })
        .fail(function (textStatus) {
            $('#loading').css("display", "none");
        });

        $.getJSON(linkREST + "consulta_convenio_cartera",
        {
            division: $("#inputDivision").val(),
            mes: $("#inputMes").val(),
        },
        function (dataTablas) {
            dataTablas.forEach(function (i) {
                $("#tablaCarteraMesA").append('<tr>' +
                    '<td>' + i.nombre + '</td>' +
                    '<td>' + i.total_mes + '</td>' +
                    '<td class="colObscuro">' + i.total_ma + '</td>' +
                    '<td>' + i.total_mes_vs_ma + '</td>' +
                    '<td class="colObscuro">' + i.total_mes_vs_ma_pct + '</td>' +
                    '</tr>');
            });

            dataTablas.forEach(function (i) {
                $("#tablaCarteraAnoA").append('<tr>' +
                    '<td>' + i.total_mes + '</td>' +
                    '<td class="colObscuro">' + i.total_maa + '</td>' +
                    '<td>' + i.total_mes_vs_maa + '</td>' +
                    '<td class="colObscuro">' + i.total_mes_vs_maa_pct + '</td>' +
                    '</tr>');
            });

            generarGraficas(
                dataTablas.map(a => a.nombre),
                dataTablas.map(a => parseInt(a.total_mes.replace(/,/g, ''))),
                generadorColores(dataTablas.length)
            )
        })
        .done(function () {
            $('#body, #titulo, #cartera').css("display", "flex");
            $('#loading').css("display", "none");
        })
        .fail(function (textStatus) {
            $('#loading').css("display", "none");
        });
}

function generarGraficas(labels, data, colors){
    graficaColocacion = new Chart($("#canvasGraficaColocacion"), {
        type: 'pie',
        options: {
            responsive: false,
            title: {
                display: true,
                position: "top",
                text: "Colocación del mes",
                fontSize: 24,
                fontColor: "#111"
            },
            legend: {
                display: true,
                position: "bottom",
                labels: {
                    fontColor: "#333",
                    fontSize: 12
                }
            },
            layout: {
                padding: {
                    left: 0, right: 0, top: 0, bottom: 0
                }
            },
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
                        var precentage = Math.floor(((currentValue / total) * 100) + 0.5);
        
                        return data.labels[tooltipItem.datasetIndex] + " : " + precentage + "% $" + currentValue.toLocaleString();
                    }
                }
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
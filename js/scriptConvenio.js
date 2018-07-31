var graficaColocacion = 0;

$(document).ready(function () {
    append = "";

    for (let i = 0; i < mes; i++) {
        append += "<option>" + (mes - i) + "/" + ano + "</option>"
    }

    for (let i = 1; i < 13; i++) {
        append += "<option>" + (13 - i) + "/" + (ano - 1) + "</option>"
    }

    $("#inputMes").append(append)
})

function getColocacion() {
    $("#tablaColocacion").html("");
    $("#tablaCarteraMesA").html("");
    $("#tablaCarteraAnoA").html("");

    if (graficaColocacion)
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
            console.log(dataTablas)

            append = "";

            for (let i = 0; i < dataTablas.length; i++) {
                if (i === dataTablas.length - 1) {
                    append += '<tr class="obscuro">' +
                        '<td>' + dataTablas[i].nombre + '</td>' +
                        '<td class="numero">$ ' + dataTablas[i].total_mes + '</td>' +
                        '<td class="colObscuro">' + dataTablas[i].total_mes_pct + '</td>' +
                        '<td class="numero">$ ' + dataTablas[i].total_mes_aa + '</td>' +
                        '<td class="colObscuro">' + dataTablas[i].total_mes_aa_pct + '</td>' +
                        '</tr>';
                }
                else {
                    append += '<tr>' +
                        '<td>' + dataTablas[i].nombre + '</td>' +
                        '<td class="numero">$ ' + dataTablas[i].total_mes + '</td>' +
                        '<td class="colObscuro">' + dataTablas[i].total_mes_pct + '</td>' +
                        '<td class="numero">$ ' + dataTablas[i].total_mes_aa + '</td>' +
                        '<td class="colObscuro">' + dataTablas[i].total_mes_aa_pct + '</td>' +
                        '</tr>';
                }
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
        });

    $.getJSON(linkREST + "consulta_convenio_cartera",
        {
            division: $("#inputDivision").val(),
            mes: $("#inputMes").val(),
        },
        function (dataTablas) {
            append = "";

            for (let i = 0; i < dataTablas.length; i++) {
                if (i === dataTablas.length - 1) {
                    append += '<tr class="obscuro">' +
                        '<td>' + dataTablas[i].nombre + '</td>' +
                        '<td class="numero">$ ' + dataTablas[i].total_mes + '</td>' +
                        '<td class="colObscuro numero">$ ' + dataTablas[i].total_ma + '</td>' +
                        '<td class="numero">$ ' + dataTablas[i].total_mes_vs_ma + '</td>' +
                        '<td class="colObscuro" style="border-right:#535353 solid 2px;">' + dataTablas[i].total_mes_vs_ma_pct + '</td>' +
                        '<td class="numero">$ ' + dataTablas[i].total_mes + '</td>' +
                        '<td class="colObscuro numero">$ ' + dataTablas[i].total_maa + '</td>' +
                        '<td class="numero">$ ' + dataTablas[i].total_mes_vs_maa + '</td>' +
                        '<td class="colObscuro">' + dataTablas[i].total_mes_vs_maa_pct + '</td>' +
                        '</tr>';
                }
                else {
                    append += '<tr >' +
                        '<td>' + dataTablas[i].nombre + '</td>' +
                        '<td class="numero">$ ' + dataTablas[i].total_mes + '</td>' +
                        '<td class="colObscuro numero">$ ' + dataTablas[i].total_ma + '</td>' +
                        '<td class="numero">$ ' + dataTablas[i].total_mes_vs_ma + '</td>' +
                        '<td class="colObscuro" style="border-right:#535353 solid 2px;">' + dataTablas[i].total_mes_vs_ma_pct + '</td>' +
                        '<td class="numero">$ ' + dataTablas[i].total_mes + '</td>' +
                        '<td class="colObscuro numero">$ ' + dataTablas[i].total_maa + '</td>' +
                        '<td  class="numero">$ ' + dataTablas[i].total_mes_vs_maa + '</td>' +
                        '<td class="colObscuro">' + dataTablas[i].total_mes_vs_maa_pct + '</td>' +
                        '</tr>';
                }
            }

            $("#tablaCarteraMesA").append(append);
        })
        .done(function () {
            $('#body, #titulo, #cartera').css("display", "flex");
            $('#loading').css("display", "none");
        })
        .fail(function (textStatus) {
            $('#loading').css("display", "none");
        });
}

function generarGraficas(labels, data, colors) {
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
                        var precentage = Math.floor((currentValue / total) * 100);
                        return labels[tooltipItem.index] + ": " + precentage + "%";
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
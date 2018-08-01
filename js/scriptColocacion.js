var graficaEstado = 0


$(document).ready(function () {
    append = "";

    for (let i = 0; i < mes; i++) {
        if(i < 10)
        {
            append += "<option> 0" + (mes - i) + "/" + ano + "</option>"
        }
        else{
            append += "<option>" + (mes - i) + "/" + ano + "</option>"
        }
    }

    for (let i = 1; i < 13; i++) {
        if(i < 4)
        {
            append += "<option>" + (13 - i) + "/" + (ano - 1) + "</option>"

        }
        else{
            append += "<option> 0" + (13 - i) + "/" + (ano - 1) + "</option>"

        }
    }

    $("#inputMes").append(append)
});


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
            append = "";
            console.log(dataTablas);

            switch (mes) {
                case 1:
                    {
                        append = "Enero";
                        break;
                    }
                case 2:
                    {
                        append = "Febrero";
                        break;
                    }
                case 3:
                    {
                        append = "Marzo";
                        break;
                    }
                case 4:
                    {
                        append = "Abril";
                        break;
                    }
                case 5:
                    {
                        append = "Mayo";
                        break;
                    }
                case 6:
                    {
                        append = "Junio";
                        break;
                    }
                case 7:
                    {
                        append = "Julio";
                        break;
                    }
                case 8:
                    {
                        append = "Agosto";
                        break;
                    }
                case 9:
                    {
                        append = "Septiembre";
                        break;
                    }
                case 10:
                    {
                        append = "Octubre";
                        break;
                    }
                case 11:
                    {
                        append = "Noviembre";
                        break;
                    }
                case 12:
                    {
                        append = "Diciembre";
                        break;
                    }
            }

            $("#tablaMesHead").append('<th colspan="3">' + append + " " + ano + "</th>");

            append = "";

            append += '<tr style="border-bottom: 4px solid #dee2e6"><td>' + dataTablas.mes[0].nombre + '</td><td class="numero">$ ' + dataTablas.mes[0].valor + '</td><td style="text-align:center;">' + dataTablas.mes[0].porcentaje + '</td></tr>';

            for (i = 1; i < dataTablas.mes.length; i++) {
                if (i === dataTablas.mes.length - 1) {
                    append += '<tr class="obscuro"><td>' + dataTablas.mes[i].nombre + '</td><td class="numero">$ ' + dataTablas.mes[i].valor + "</td><td>" + dataTablas.mes[i].porcentaje + "</td></tr>";
                }
                else {
                    append += '<tr><td>' + dataTablas.mes[i].nombre + '</td><td class="numero">$ ' + dataTablas.mes[i].valor + "</td><td>" + dataTablas.mes[i].porcentaje + "</td></tr>";
                }
            }

            $("#tablaMesBody").append(append);

            append = "";

            append += '<tr style="border-bottom: 4px solid #dee2e6"><td>' + dataTablas.acumulado[0].nombre + '</td><td class="numero">$ ' + dataTablas.acumulado[0].valor + '</td><td style="text-align:center;">' + dataTablas.acumulado[0].porcentaje + '</td></tr>';

            for (i = 1; i < dataTablas.acumulado.length; i++) {
                if (i === dataTablas.acumulado.length - 1) {
                    append += '<tr class="obscuro"><td>' + dataTablas.acumulado[i].nombre + '</td><td class="numero">$ ' + dataTablas.acumulado[i].valor + "</td><td>" + dataTablas.acumulado[i].porcentaje + "</td></tr>";
                }
                else {
                    append += '<tr><td>' + dataTablas.acumulado[i].nombre + '</td><td class="numero">$ ' + dataTablas.acumulado[i].valor + "</td><td>" + dataTablas.acumulado[i].porcentaje + "</td></tr>";
                }
            }

            $("#tablaAcumuladoBody").append(append);

            append = "";

            for (i = 0; i < dataTablas.costo.length; i++) {
                if (i === dataTablas.costo.length - 1) {
                    append += '<tr class="obscuro"><td style="width = 100px;">' + dataTablas.costo[i].nombre + '</td><td style="width = 100px;">' + dataTablas.costo[i].porcentaje + "</td></tr>";
                }
                else {
                    append += '<tr><td style="width = 100px;">' + dataTablas.costo[i].nombre + ' </td><td style="width = 100px;">' + dataTablas.costo[i].porcentaje + "</td></tr>";
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

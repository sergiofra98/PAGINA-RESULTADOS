var graficaEstado = 0

$(document).ready(function () {

    for (let i = 1; i < mes + 1; i++) {


        if (i === mes) {
            $("#inputMes").append('<option selected value="' + i + '">' + i + '</option>')
        }
        else {
            $("#inputMes").append('<option value="' + i + '">' + i + '</option>')
        }

    }

    $("#ano").append(
        "/ " + ano
    )

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

            append += '<tr style="border-bottom: 4px solid #dee2e6"><td>' + dataTablas.mes[0].nombre + '</td><td style="text-align:center;">' + dataTablas.mes[0].porcentaje + "</td><td>" + dataTablas.mes[0].valor + '</td></tr>';

            for (i = 1; i < dataTablas.mes.length; i++) {
                if (i === dataTablas.mes.length - 1) {
                    append += '<tr class="obscuro"><td>' + dataTablas.mes[i].nombre + "</td><td>" + dataTablas.mes[i].porcentaje + "</td><td>" + dataTablas.mes[i].valor + "</td></tr>";
                }
                else {
                    append += '<tr><td>' + dataTablas.mes[i].nombre + "</td><td>" + dataTablas.mes[i].porcentaje + "</td><td>" + dataTablas.mes[i].valor + "</td></tr>";
                }
            }

            $("#tablaMesBody").append(append);

            append = "";

            append += '<tr style="border-bottom: 4px solid #dee2e6"><td>' + dataTablas.acumulado[0].nombre + '</td><td style="text-align:center;">' + dataTablas.acumulado[0].porcentaje + "</td><td>" + dataTablas.acumulado[0].valor + '</td></tr>';

            for (i = 1; i < dataTablas.acumulado.length; i++) {
                if (i === dataTablas.acumulado.length - 1) {
                    append += '<tr class="obscuro"><td>' + dataTablas.acumulado[i].nombre + "</td><td>" + dataTablas.acumulado[i].porcentaje + "</td><td>" + dataTablas.acumulado[i].valor + "</td></tr>";
                }
                else {
                    append += '<tr><td>' + dataTablas.acumulado[i].nombre + "</td><td>" + dataTablas.acumulado[i].porcentaje + "</td><td>" + dataTablas.acumulado[i].valor + "</td></tr>";
                }
            }

            $("#tablaAcumuladoBody").append(append);

            append = "";

            for (i = 0; i < dataTablas.costo.length; i++) {
                if (i === dataTablas.costo.length - 1) {
                    append += '<tr class="obscuro"><td>' + dataTablas.costo[i].nombre + "</td><td>" + dataTablas.costo[i].porcentaje + "</td></tr>";
                }
                else {
                    append += '<tr><td>' + dataTablas.costo[i].nombre + "</td><td>" + dataTablas.costo[i].porcentaje + "</td></tr>";
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
                    labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
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
                text: 'Colocación por estado'
            },
            legend: { display: false },
            elements: {
                line: {
                    tension: 0, // disables bezier curves
                }
            },
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

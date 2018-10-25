var linkREST = "http://127.0.0.1:9999/MasNomina/MonitorVentas/";
var currentTime = new Date();
var mes = currentTime.getMonth();
var ano = currentTime.getFullYear();

function obtenerDivisiones(){
    $.getJSON(linkREST + "consulta_divisiones", {},
        function (dataTablas) {

            var append = '<option disabled="" hidden="" selected="" value="">Elija una opción</option>'
            append += '<option value="0">TODAS</option>'

            for(let i = 0; i < dataTablas.length; i++){
                append += '<option value="' + dataTablas[i][0] +'">' + dataTablas[i][1] +'</option>'
            }

            $('#inputDivision').html(append)
         })
        .done(function () {
        })
        .fail(function (textStatus) {
        });


}

$(document).ready(function () {
    obtenerDivisiones()

    append = "<option hidden selected disabled>Elija un Periodo</option>";
    let i = 0
    let flex = 0
    let band = false
    for (i; i < 13; i++) {
        flex = mes - i
        if (i === mes) {
            band = true
        }

        if (band) {
            append += '<option value="' + (ano - 1) + formatearMes(flex + 12) + '">' + formatearMes(flex + 12) + '/' + (ano - 1) + "</option>";
        }
        else {
            append += '<option value="' + ano + formatearMes(flex) + '">' + formatearMes(flex) + '/' + ano + "</option>";
        }
    }

    $("#inputFecha").append(append)

});

function formatearMes(mes) {
    if (mes < 10) {
        return "0" + mes
    }
    else {
        return mes
    }
}

function generadorColores(num) {
    arr = [];

    listCol = ["#4286f4", "#6bf441", "#f45e41", "#f4df41", "#ff2626", "#63d88c",
        "#003459", "#9A348E", "#F9DBBD", "#6622CC", "#462521", "#CA2E55", "#717EC3",
        "#EE8434", "#284B63", "#B4B8AB", "#FED766", "#161B33", "#B0CA87", "#2E0014",
        "#755896", "#1d7a6d", "#6a8c13", "#e243e8", "#ce8c82", "#004577", "#a81c64"];

    for (let i = 0; i < num; i++) {
        if (listCol[i] != undefined)
            arr.push(listCol[i])
    }

    return arr;
};

function generadorColoresUno(num) {

    listCol = ["#4286f4", "#6bf441", "#f45e41", "#f4df41", "#ff2626", "#63d88c",
        "#003459", "#9A348E", "#F9DBBD", "#6622CC", "#462521", "#CA2E55", "#717EC3",
        "#EE8434", "#284B63", "#B4B8AB", "#FED766", "#161B33", "#B0CA87", "#2E0014",
        "#755896", "#1d7a6d", "#6a8c13", "#e243e8", "#ce8c82", "#004577", "#a81c64"];

    return listCol[num];
};

function getStringMes(i) {
    switch (i) {
        case 0:
            {
                return "ENE";
            }
        case 1:
            {
                return "FEB";
            }
        case 2:
            {
                return "MAR";
            }
        case 3:
            {
                return "ABR";
            }
        case 4:
            {
                return "MAY";
            }
        case 5:
            {
                return "JUN";
            }
        case 6:
            {
                return "JUL";
            }
        case 7:
            {
                return "AGO";
            }
        case 8:
            {
                return "SEP";
            }
        case 9:
            {
                return "OCT";
            }
        case 10:
            {
                return "NOV";
            }
        case 11:
            {
                return "DIC";
            }
    }
}

function cerrarAlerta(event) {
    var modi = $(event.currentTarget).parent();

    modi.css('display', 'none');
}


function iniciarBusqueda() {
    $(".alert").css('display', 'none')

    if (!$('#inputFecha').val() || !$('#inputDivision').val() || !$('#inputProducto').val()) {
        $("#alertaValidacion").css('display', 'block')
    }
    else {
        getColocacion()
    }
}
function iniciarBusquedaEstado() {
    $(".alert").css('display', 'none')

    if (!$('#inputFecha').val() || !$('#inputDivision').val()) {
        $("#alertaValidacion").css('display', 'block')
    }
    else {
        getColocacion()
    }
}
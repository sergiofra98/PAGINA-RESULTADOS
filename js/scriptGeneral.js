var linkREST = "http://127.0.0.1:9999/MasNomina/MonitorVentas/";
var currentTime = new Date();
var mes = currentTime.getMonth();
var ano = currentTime.getFullYear();

$(document).ready(function () {
    append = "<option hidden selected disabled>Mes</option>";

    for (let i = 0; i < 12; i++) {
            append += "<option>" + getStringMes(i) + "</option>"
    }

    $("#inputMes").append(append)

    append = "<option hidden selected disabled>Año</option>";

    for (let i = 0; i < 6; i++) {
        append += "<option> " + (ano - i) + "</option>"
    }

    $("#inputAno").append(append)

});

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
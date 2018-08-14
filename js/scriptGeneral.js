var linkREST = "http://127.0.0.1:9999/MasNomina/MonitorVentas/";
var currentTime = new Date();
var mes = currentTime.getMonth();
var ano = currentTime.getFullYear();

$(document).ready(function () {
    append = "";

    for (let i = 0; i < 12; i++) {
        if(i === mes)
        {
            append += "<option selected>" + getStringMes(i) + "</option>"
        }
        else {
            append += "<option>" + getStringMes(i) + "</option>"
        }
    }

    $("#inputMes").append(append)

    append = "";

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
                return "Enero";

            }
        case 1:
            {
                return "Febrero";
            }
        case 2:
            {
                return "Marzo";
            }
        case 3:
            {
                return "Abril";
            }
        case 4:
            {
                return "Mayo";
            }
        case 5:
            {
                return "Junio";
            }
        case 6:
            {
                return "Julio";
            }
        case 7:
            {
                return "Agosto";
            }
        case 8:
            {
                return "Septiembre";
            }
        case 9:
            {
                return "Octubre";
            }
        case 10:
            {
                return "Noviembre";
            }
        case 11:
            {
                return "Diciembre";
            }
    }
}
var linkREST = "http://127.0.0.1:9999/MasNomina/MonitorVentas/";
var currentTime = new Date();
var mes = currentTime.getMonth() + 1;
var ano = currentTime.getFullYear();

function generadorColores(num) {
    arr = [];

    listCol = ["#4286f4", "#6bf441", "#f45e41", "#f4df41", "#ff2626", "#63d88c",
    "#003459", "#9A348E", "#F9DBBD", "#6622CC", "#462521", "#CA2E55", "#717EC3",
    "#EE8434", "#284B63", "#B4B8AB", "#FED766", "#161B33", "#B0CA87", "#2E0014",
    "#755896", "#1d7a6d", "#6a8c13", "#e243e8", "#ce8c82", "#004577", "#a81c64"];

    for (let i = 0; i < num; i++) {
        if(listCol[i] != undefined)
            arr.push(listCol[i])
    }

    return arr;
};
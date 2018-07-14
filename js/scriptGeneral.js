var linkREST = "http://127.0.0.1:9999/MasNomina/MonitorVentas/";
var currentTime = new Date();
var mes = currentTime.getMonth() + 1;
var ano = currentTime.getFullYear();

function generadorColores(num) {
    arr = [];

    for (let i = 0; i < num; i++) {
        arr.push('rgb(' + Math.round(Math.random() * 255) + ',' + Math.round(Math.random() * 255) + ',' + Math.round(Math.random() * 255) + ')')
    }

    return arr;
};
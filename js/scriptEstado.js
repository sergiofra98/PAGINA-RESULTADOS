var linkREST = "http://127.0.0.1:9999/MasNomina/MonitorVentas/";
var graficaColocacion;
var options = {
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
};

$(document).ready(function () {
    graficaColocacion = new Chart($("#canvasGraficaColocacion"), {
        type: 'pie',
        options: 0,
        data: 0
    });;
});



function generadorColores(num) {
    arr = [];

    for (let i = 0; i < num; i++) {
        arr.push('rgb(' + Math.round(Math.random() * 255) + ',' + Math.round(Math.random() * 255) + ',' + Math.round(Math.random() * 255) + ')')
    }

    return arr;
};


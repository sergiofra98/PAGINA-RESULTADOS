

$(document).ready(function () {
    var ctx = $("#canvasGraficaColocacion");

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

                    return data.labels[tooltipItem.datasetIndex] + " : " + precentage + "%";
                }
            }
        }
    };

    data = {
        datasets: [{
            data: [
                45,
                16,
                14,
                10,
                7,
                3,
                3,
                2,
                0
            ],
            backgroundColor: [
                "#FF6384",
                "#4BC0C0",
                "#FFCE56",
                "#E7E9ED",
                "#36A2EB"
            ],
            label: 'My dataset' // for legend
        }],
        labels: [
            "Gobierno de Hidalgo",
            "SNTE 14",
            "PEMEX",
            "SAGARPA",
            "INE",
            "SNTE 23 PUEBLA",
            "IMSS PENSIONES",
            "IMSS JUBILADOS",
            "IMSS ACTIVOS"
        ]
    };


    var myPieChart = new Chart(ctx, {
        type: 'pie',
        data: data,
        options: options
    });

    console.log(2);
});

var randomColor = function (opacity) {
    return 'rgba(' + randomColorFactor() + ',' + randomColorFactor() + ',' + randomColorFactor() + ',' + (opacity || '.3') + ')';
};

var randomColorFactor = function () {
    return Math.round(Math.random() * 255);
};
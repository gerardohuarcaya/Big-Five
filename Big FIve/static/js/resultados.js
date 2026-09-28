window.onload = function () {

    console.log("Informe generado correctamente.");

};

function imprimir() {

    window.print();

}


const tarjetas = document.querySelectorAll(".card");

tarjetas.forEach((tarjeta, i) => {

    tarjeta.style.animationDelay = (i * 0.2) + "s";

});

console.log(datosBigFive);


const rasgos = {
    "Apertura": datosBigFive.apertura,
    "Responsabilidad": datosBigFive.responsabilidad,
    "Extraversión": datosBigFive.extroversion,
    "Amabilidad": datosBigFive.amabilidad,
    "Neuroticismo": datosBigFive.neuroticismo
};

let rasgoDominante = "";

let mayor = 0;

for (let rasgo in rasgos) {

    if (rasgos[rasgo] > mayor) {

        mayor = rasgos[rasgo];
        rasgoDominante = rasgo;

    }

}

console.log("Rasgo dominante:", rasgoDominante);
console.log("Puntaje:", mayor);

const ctx = document.getElementById("graficoBigFive");

if (ctx) {

    new Chart(ctx, {

        type: "radar",

        data: {

            labels: [

                "Apertura",
                "Responsabilidad",
                "Extraversión",
                "Amabilidad",
                "Neuroticismo"

            ],

            datasets: [

                {

                    label: "Perfil Big Five",

                    data: [

                        datosBigFive.apertura,
                        datosBigFive.responsabilidad,
                        datosBigFive.extroversion,
                        datosBigFive.amabilidad,
                        datosBigFive.neuroticismo

                    ],

                    backgroundColor: "rgba(37,99,235,0.2)",

                    borderColor: "#2563eb",

                    borderWidth: 3,

                    pointBackgroundColor: "#2563eb",

                    pointBorderColor: "#ffffff",

                    pointRadius: 6,

                    pointHoverRadius: 8

                }

            ]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    position: "top"

                }

            },

            scales: {

                r: {

                    min: 0,

                    max: 5,

                    ticks: {

                        stepSize: 1,

                        backdropColor: "transparent"

                    },

                    grid: {

                        color: "#cccccc"

                    },

                    angleLines: {

                        color: "#dddddd"

                    },

                    pointLabels: {

                        font: {

                            size: 14,

                            weight: "bold"

                        }

                    }

                }

            },

            animation: {

                duration: 1800

            }

        }

    });

}
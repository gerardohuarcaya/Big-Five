window.onload = function() {
    console.log("Página cargada correctamente.");
}

const nombre = document.getElementById("nombre");

nombre.addEventListener("input", function() {
    console.log("Nombre:", nombre.value);
});

const correo = document.getElementById("correo");

correo.addEventListener("blur", function() {

    if (!correo.value.includes("@")) {
        alert("Ingrese un correo válido.");
    }

});

const formulario = document.querySelector("form");

formulario.addEventListener("submit", function() {
    alert("Procesando respuestas...");
});

const radios = document.querySelectorAll('input[type="radio"]');

radios.forEach(radio => {

    radio.addEventListener("change", contar);

});

function contar() {

    let respondidas = 0;

    for (let i = 1; i <= 5; i++) {

        if (document.querySelector(`input[name="p${i}"]:checked`)) {

            respondidas++;

        }

    }

    document.getElementById("progreso").textContent =
        `Preguntas respondidas: ${respondidas}/5`;

    document.getElementById("avance").style.width =
        (respondidas / 5 * 100) + "%";

}

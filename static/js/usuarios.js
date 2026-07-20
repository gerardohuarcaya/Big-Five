const buscar = document.getElementById("buscar");

buscar.addEventListener("keyup", function () {

    const texto = buscar.value.toLowerCase();

    const filas = document.querySelectorAll("#tablaUsuarios tbody tr");

    filas.forEach(fila => {

        const contenido = fila.textContent.toLowerCase();

        fila.style.display = contenido.includes(texto) ? "" : "none";

    });

});
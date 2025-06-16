document.addEventListener("DOMContentLoaded", function () {
    const tipoPruebaSelect = document.getElementById("tipo-prueba");
    const cableSetInput = document.getElementById("cable-set");
    const contenedorResultados = document.getElementById("contenedor-resultados");

    tipoPruebaSelect.addEventListener("change", generarCampos);
    cableSetInput.addEventListener("input", generarCampos);

    function generarCampos() {
        const tipo = tipoPruebaSelect.value;
        const cantidad = parseInt(cableSetInput.value) || 0;
        contenedorResultados.innerHTML = "";

        const pruebasContinuidad = ["L1", "L2", "L3", "N", "E"];
        const pruebasMegado = ["L1-L2", "L1-L3", "L2-L3", "L1-N", "L2-N", "L3-N", "L1-E", "L2-E", "L3-E", "N-E"];

        for (let i = 1; i <= cantidad; i++) {
            const tabla = document.createElement("table");
            tabla.classList.add("tabla-prueba");

            const caption = document.createElement("caption");
            caption.textContent = `${tipo} - Cable Set ${i}`;
            tabla.appendChild(caption);

            const encabezado = document.createElement("tr");
            encabezado.innerHTML = `
                <th>Punto de prueba</th>
                <th>Valor de referencia</th>
                <th>Resultado</th>
                <th>¿Aprobado?</th>
                <th>Imagen</th>
            `;
            tabla.appendChild(encabezado);

            const pruebas = tipo === "continuidad" ? pruebasContinuidad : pruebasMegado;

            pruebas.forEach((punto, idx) => {
                const fila = document.createElement("tr");

                fila.innerHTML = `
                    <td>${punto}</td>
                    <td><input name="referencia_${i}_${punto}" type="text" /></td>
                    <td><input name="resultado_${i}_${punto}" type="text" /></td>
                    <td><input name="aprobado_${i}_${punto}" type="checkbox" /></td>
                    <td>
                        <label class="camera-label">
                            📷
                            <input type="file" accept="image/*" capture="environment"
                                   name="imagen_${i}_${punto}" style="display: none;">
                        </label>
                    </td>
                `;
                tabla.appendChild(fila);
            });

            contenedorResultados.appendChild(tabla);
        }
    }
});

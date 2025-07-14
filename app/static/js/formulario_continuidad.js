function initFormularioContinuidad(tipoAlimentacion) {
    const cableSetInput = document.getElementById("cable_sets");
    const referenciaComunInput = document.getElementById("referencia-comun");
    const contenedorResultados = document.getElementById("contenedor-resultados");
    const bloqueResultados = document.getElementById("bloque-resultados");
    const unidadSelect = document.getElementById("unidad");

    const conductores = tipoAlimentacion === "monofasica"
        ? ["L", "N", "PE"]
        : ["L1", "L2", "L3", "N", "PE"];

    const combinaciones = conductores;

    function validarAprobado(valor, referencia) {
        if (!valor || valor.toLowerCase() === "n/a") return true;
        const num = parseFloat(valor);
        const ref = parseFloat(referencia);
        if (isNaN(num) || isNaN(ref)) return false;
        return num <= ref;
    }

    function generarCampos() {
        const cantidad = parseInt(cableSetInput.value) || 0;
        const unidad = unidadSelect.value;
        const referencia = referenciaComunInput.value;
        contenedorResultados.innerHTML = "";
        bloqueResultados.style.display = cantidad > 0 ? "block" : "none";

        for (let i = 1; i <= cantidad; i++) {
            const tabla = document.createElement("table");
            tabla.classList.add("tabla-prueba");
            tabla.innerHTML = `
                <caption>Contact Resistance - Cable Set ${i}</caption>
                <tr>
                    <th>Punto</th>
                    <th>Resultado</th>
                    <th>Unidad</th>
                    <th>¿Aprobado?</th>
                    <th>Observaciones</th>
                    <th>Imagen</th>
                </tr>`;

            combinaciones.forEach((punto) => {
                const idResultado = `resultado_${i}_${punto}`;
                const idNA = `na_${i}_${punto}`;
                const idAprobado = `aprobado_${i}_${punto}`;

                const fila = document.createElement("tr");
                fila.innerHTML = `
                    <td>${punto}</td>
                    <td>
                        <div class="resultado-combinado">
                            <button type="button" class="na-btn" id="${idNA}">N/A</button>
                            <input type="text" name="${idResultado}" id="${idResultado}" />
                        </div>
                    </td>
                    <td><input name="unidad_${i}_${punto}" type="text" value="${unidad}" readonly /></td>
                    <td><input id="${idAprobado}" name="aprobado_${i}_${punto}" type="checkbox" disabled /></td>
                    <td><input name="observaciones_${i}_${punto}" type="text" /></td>
                    <td>
                        <label class="camera-label">
                            📷 <span class="adjunto-texto"></span>
                            <input type="file" accept="image/*" name="imagen_${i}_${punto}" style="display:none;" />
                        </label>
                    </td>
                `;
                tabla.appendChild(fila);

                const inputResultado = fila.querySelector(`#${idResultado}`);
                const botonNA = fila.querySelector(`#${idNA}`);
                const checkboxAprobado = fila.querySelector(`#${idAprobado}`);

                if (botonNA && inputResultado && checkboxAprobado) {
                    botonNA.addEventListener("click", () => {
                        if (inputResultado.disabled) {
                            inputResultado.disabled = false;
                            inputResultado.value = "";
                            botonNA.classList.remove("activo");
                        } else {
                            inputResultado.disabled = true;
                            inputResultado.value = "N/A";
                            botonNA.classList.add("activo");
                            checkboxAprobado.checked = true;
                            checkboxAprobado.classList.add("verde");
                        }
                    });
                }

                const actualizarAprobado = () => {
                    if (checkboxAprobado && inputResultado) {
                        const aprobado = validarAprobado(inputResultado.value, referencia);
                        checkboxAprobado.checked = aprobado;
                        checkboxAprobado.classList.toggle("verde", aprobado);
                    }
                };

                inputResultado?.addEventListener("input", actualizarAprobado);

                const label = fila.querySelector("label");
                const inputFile = label?.querySelector("input[type='file']");
                const textoAdjunto = label?.querySelector(".adjunto-texto");

                inputFile?.addEventListener("change", async (e) => {
                    const file = e.target.files[0];
                    textoAdjunto.textContent = file ? "📎 Archivo adjunto" : "";
                });
            });

            contenedorResultados.appendChild(tabla);
        }
    }

    cableSetInput.addEventListener("input", generarCampos);
    unidadSelect.addEventListener("change", generarCampos);
    referenciaComunInput.addEventListener("input", generarCampos);
    generarCampos();
}

window.initFormularioContinuidad = initFormularioContinuidad;

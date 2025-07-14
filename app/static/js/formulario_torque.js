function initFormularioTorque(tipoAlimentacion) {
    const cableSetInput = document.getElementById("cable_sets");
    const contenedorResultados = document.getElementById("contenedor-resultados");
    const bloqueResultados = document.getElementById("bloque-resultados");
    const unidadSelect = document.getElementById("unidad");

    const conductores = tipoAlimentacion === "monofasica"
        ? ["L", "N", "PE"]
        : ["L1", "L2", "L3", "N", "PE"];

    function validarAprobado(nominal, comprobacion) {
        const n = parseFloat(nominal);
        const c = parseFloat(comprobacion);
        if (isNaN(n) || isNaN(c)) return false;
        const tolerancia = 0.1 * n;
        return c >= n - tolerancia && c <= n + tolerancia;
    }

    function generarCampos() {
        const cantidad = parseInt(cableSetInput.value) || 0;
        const unidad = unidadSelect.value;
        contenedorResultados.innerHTML = "";
        bloqueResultados.style.display = cantidad > 0 ? "block" : "none";

        for (let i = 1; i <= cantidad; i++) {
            const tabla = document.createElement("table");
            tabla.classList.add("tabla-prueba");
            tabla.innerHTML = `
                <caption>Torque - Cable Set ${i}</caption>
                <tr>
                    <th>Punto</th>
                    <th>Valor Nominal</th>
                    <th>Valor Comprobación / N/A</th>
                    <th>Unidad</th>
                    <th>¿Aprobado?</th>
                    <th>Observaciones</th>
                    <th>Imagen</th>
                </tr>`;

            conductores.forEach((punto) => {
                const idNominal = `nominal_${i}_${punto}`;
                const idComprobacion = `comprobacion_${i}_${punto}`;
                const idNA = `na_${i}_${punto}`;
                const idAprobado = `aprobado_${i}_${punto}`;

                const fila = document.createElement("tr");
                fila.innerHTML = `
                    <td>${punto}</td>
                    <td><input name="${idNominal}" type="text" /></td>
                    <td>
                        <div class="resultado-combinado">
                            <button type="button" class="na-btn" id="${idNA}">N/A</button>
                            <input type="text" name="${idComprobacion}" id="${idComprobacion}" />
                        </div>
                    </td>
                    <td><input name="unidad_${i}_${punto}" type="text" value="${unidad}" readonly /></td>
                    <td><input id="${idAprobado}" name="${idAprobado}" type="checkbox" disabled /></td>
                    <td><input name="observaciones_${i}_${punto}" type="text" /></td>
                    <td>
                        <label class="camera-label">
                            📷 <span class="adjunto-texto"></span>
                            <input type="file" accept="image/*" name="imagen_${i}_${punto}" style="display:none;" />
                        </label>
                    </td>
                `;
                tabla.appendChild(fila);

                const inputNominal = fila.querySelector(`input[name="${idNominal}"]`);
                const inputComprobacion = fila.querySelector(`#${idComprobacion}`);
                const botonNA = fila.querySelector(`#${idNA}`);
                const checkboxAprobado = fila.querySelector(`#${idAprobado}`);

                if (botonNA && inputComprobacion && checkboxAprobado) {
                    botonNA.addEventListener("click", () => {
                        if (inputComprobacion.disabled) {
                            inputComprobacion.disabled = false;
                            inputComprobacion.value = "";
                            botonNA.classList.remove("activo");
                        } else {
                            inputComprobacion.disabled = true;
                            inputComprobacion.value = "N/A";
                            botonNA.classList.add("activo");
                            checkboxAprobado.checked = true;
                            checkboxAprobado.classList.add("verde");
                        }
                    });
                }

                const actualizarAprobado = () => {
                    if (checkboxAprobado && inputNominal && inputComprobacion) {
                        const aprobado = validarAprobado(inputNominal.value, inputComprobacion.value);
                        checkboxAprobado.checked = aprobado;
                        checkboxAprobado.classList.toggle("verde", aprobado);
                    }
                };

                inputNominal.addEventListener("input", actualizarAprobado);
                inputComprobacion?.addEventListener("input", actualizarAprobado);

                const label = fila.querySelector("label");
                const inputFile = label.querySelector("input[type='file']");
                const textoAdjunto = label.querySelector(".adjunto-texto");

                inputFile.addEventListener("change", () => {
                    textoAdjunto.textContent = inputFile.files.length > 0 ? "📎 Archivo adjunto" : "";
                });
            });

            contenedorResultados.appendChild(tabla);
        }
    }

    cableSetInput.addEventListener("input", generarCampos);
    unidadSelect.addEventListener("change", generarCampos);
    generarCampos();
}

window.initFormularioTorque = initFormularioTorque;

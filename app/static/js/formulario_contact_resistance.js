function initFormularioContactResistance(tipoAlimentacion) {
    const cableSetInput = document.getElementById("cable_sets");
    const referenciaComunInput = document.getElementById("referencia-comun");
    const contenedorResultados = document.getElementById("contenedor-resultados");
    const bloqueResultados = document.getElementById("bloque-resultados");
    const unidadSelect = document.getElementById("unidad");

    if (!cableSetInput || !referenciaComunInput || !contenedorResultados || !bloqueResultados || !unidadSelect) {
        console.error("Formulario contact resistance: elementos requeridos no encontrados.");
        return;
    }

    const conductores = tipoAlimentacion === "monofasica"
        ? ["L", "N", "PE"]
        : ["L1", "L2", "L3", "N", "PE"];

    const generarCombinaciones = (lista) => {
        const combos = [];
        for (let i = 0; i < lista.length; i++) {
            for (let j = i + 1; j < lista.length; j++) {
                combos.push(`${lista[i]}-${lista[j]}`);
            }
        }
        return combos;
    };

    const combinaciones = generarCombinaciones(conductores);

    const validarAprobadoContact = (valor, referencia) => {
        if (!valor || valor.toLowerCase() === "n/a") return true;
        const num = parseFloat(valor);
        const ref = parseFloat(referencia);
        return !isNaN(num) && !isNaN(ref) && num <= ref;
    };

    function generarCampos() {
        const cantidad = parseInt(cableSetInput.value) || 0;
        const referenciaComun = referenciaComunInput.value;
        const unidad = unidadSelect.value;
        contenedorResultados.innerHTML = "";
        bloqueResultados.style.display = cantidad > 0 ? "block" : "none";

        for (let i = 1; i <= cantidad; i++) {
            const tabla = document.createElement("table");
            tabla.classList.add("tabla-prueba");

            tabla.innerHTML = `
                <caption>Contact Resistance - Cable Set ${i}</caption>
                <tr>
                    <th>Punto</th>
                    <th>Referencia</th>
                    <th>Resultado / N/A</th>
                    <th>Unidad</th>
                    <th>¿Aprobado?</th>
                    <th>Observaciones</th>
                    <th>Imagen</th>
                </tr>`;

            combinaciones.forEach((punto) => {
                const fila = document.createElement("tr");
                const idResultado = `resultado_${i}_${punto}`;
                const idNA = `na_${i}_${punto}`;
                const idUnidad = `unidad_${i}_${punto}`;
                const idAprobado = `aprobado_${i}_${punto}`;

                fila.innerHTML = `
                    <td>${punto}</td>
                    <td>${referenciaComun} ${unidad}</td>
                    <td>
                      <div class="resultado-combinado">
                        <button type="button" class="na-btn" id="${idNA}">N/A</button>
                        <input type="text" name="${idResultado}" id="${idResultado}" />
                      </div>
                    </td>
                    <td><input name="${idUnidad}" type="text" value="${unidad}" readonly /></td>
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
                        const isDisabled = inputResultado.disabled;
                        inputResultado.disabled = !isDisabled;
                        inputResultado.value = isDisabled ? "" : "N/A";
                        botonNA.classList.toggle("activo", !isDisabled);
                        checkboxAprobado.checked = !isDisabled;
                        checkboxAprobado.classList.toggle("verde", !isDisabled);
                    });
                }

                inputResultado?.addEventListener("input", () => {
                    const aprobado = validarAprobadoContact(inputResultado.value, referenciaComun);
                    checkboxAprobado.checked = aprobado;
                    checkboxAprobado.classList.toggle("verde", aprobado);
                });

                const label = fila.querySelector("label");
                const inputFile = label?.querySelector("input[type='file']");
                const textoAdjunto = label?.querySelector(".adjunto-texto");

                inputFile?.addEventListener("change", (e) => {
                    const file = e.target.files[0];
                    textoAdjunto.textContent = file ? "📎 Archivo adjunto" : "";
                });
            });

            contenedorResultados.appendChild(tabla);
        }
    }

    cableSetInput.addEventListener("input", generarCampos);
    referenciaComunInput.addEventListener("input", generarCampos);
    unidadSelect.addEventListener("change", generarCampos);
    generarCampos();
}

window.initFormularioContactResistance = initFormularioContactResistance;

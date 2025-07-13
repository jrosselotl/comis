function initFormularioContactResistance(tipoAlimentacion) {
    const cableSetInput = document.getElementById("cable_sets");
    const referenciaComunInput = document.getElementById("referencia-comun");
    const contenedorResultados = document.getElementById("contenedor-resultados");
    const bloqueResultados = document.getElementById("bloque-resultados");
    const unidadSelect = document.getElementById("unidad-select");

    if (!cableSetInput || !referenciaComunInput || !contenedorResultados || !bloqueResultados || !unidadSelect) {
        return;
    }

    const conductores = tipoAlimentacion === "monofasica"
        ? ["L", "N", "PE"]
        : ["L1", "L2", "L3", "N", "PE"];

    const combinaciones = conductores; // NO combinaciones cruzadas

    function validarAprobadoContact(valor, referencia) {
        if (!valor || valor.toLowerCase() === "n/a") return true;
        const num = parseFloat(valor);
        const ref = parseFloat(referencia);
        if (isNaN(num) || isNaN(ref)) return false;
        return num <= ref;
    }

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
                        const aprobado = validarAprobadoContact(inputResultado.value, referenciaComun);
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
    referenciaComunInput.addEventListener("input", generarCampos);
    unidadSelect.addEventListener("change", generarCampos);
    generarCampos();

    document.getElementById("formulario-pruebas").addEventListener("submit", async function (e) {
        const tipo = document.getElementById("tipo-prueba")?.value;
        if (tipo !== "contact_resistance") return;

        e.preventDefault();

        const cableSets = parseInt(cableSetInput.value);
        const unidad = unidadSelect.value;
        const referenciaComun = referenciaComunInput.value;

        if (!cableSets || !unidad || !referenciaComun) {
            alert("Debe ingresar Cable Sets, unidad y valor de referencia.");
            return;
        }

        const datos = [];
        const imagenes = [];

        const proyecto_id = document.getElementById("proyecto_id").value;
        const ubicacion_1 = document.getElementById("ubicacion_1").value;
        const numero_ubicacion_1 = document.getElementById("numero_ubicacion_1").value;
        const ubicacion_2 = document.getElementById("ubicacion_2")?.value || "";
        const numero_ubicacion_2 = document.getElementById("numero_ubicacion_2")?.value || "";
        const tipo_equipo = document.getElementById("tipo_equipo").value;
        const numero_tipo_equipo = document.getElementById("numero_tipo_equipo").value;
        const sub_equipo = document.getElementById("sub_equipo")?.value || "";
        const numero_sub_equipo = document.getElementById("numero_sub_equipo")?.value || "";
        const tipo_alimentacion = document.getElementById("tipo_alimentacion")?.value;
        const terminal = document.getElementById("terminal")?.value || "";
        const test_id = document.getElementById("tipo-prueba").selectedOptions[0]?.getAttribute("data-id");

        for (let i = 1; i <= cableSets; i++) {
            for (const punto of combinaciones) {
                const resultado = document.querySelector(`[name="resultado_${i}_${punto}"]`)?.value || "";
                const observaciones = document.querySelector(`[name="observaciones_${i}_${punto}"]`)?.value || "";
                const imagenInput = document.querySelector(`[name="imagen_${i}_${punto}"]`);
                const imagen = imagenInput?.files[0];

                datos.push({
                    cable_set: i,
                    punto_prueba: punto,
                    referencia_valor: referenciaComun,
                    resultado_valor: resultado,
                    unidad: unidad,
                    observaciones: observaciones
                });

                imagenes.push(imagen || new File([], ""));
            }
        }

        const formData = new FormData();
        formData.append("proyecto_id", proyecto_id);
        formData.append("ubicacion_1", ubicacion_1);
        formData.append("numero_ubicacion_1", numero_ubicacion_1);
        formData.append("ubicacion_2", ubicacion_2);
        formData.append("numero_ubicacion_2", numero_ubicacion_2);
        formData.append("tipo_equipo", tipo_equipo);
        formData.append("numero_tipo_equipo", numero_tipo_equipo);
        formData.append("sub_equipo", sub_equipo);
        formData.append("numero_sub_equipo", numero_sub_equipo);
        formData.append("test_id", test_id);
        formData.append("cable_sets", cableSets);
        formData.append("tipo_alimentacion", tipo_alimentacion);
        formData.append("terminal", terminal);
        formData.append("datos", JSON.stringify(datos));
        imagenes.forEach(img => formData.append("imagenes", img));

        const response = await fetch("/formulario/guardar", {
            method: "POST",
            body: formData
        });

        const res = await response.json().catch(() => null);
        if (response.ok && res?.mensaje) {
            alert(res.mensaje);
        } else {
            alert(res?.detail || "Error al guardar el formulario.");
        }
    });
}

window.initFormularioContactResistance = initFormularioContactResistance;

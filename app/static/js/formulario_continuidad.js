function initFormularioContinuidad(tipoAlimentacion) {
    const cableSetInput = document.getElementById("cable_sets");
    const contenedorResultados = document.getElementById("contenedor-resultados");
    const bloqueResultados = document.getElementById("bloque-resultados");

    const conductores = tipoAlimentacion === "monofasica"
        ? ["L", "N", "PE"]
        : ["L1", "L2", "L3", "N", "PE"];

    function generarCombinaciones(lista) {
        const combos = [];
        for (let i = 0; i < lista.length; i++) {
            for (let j = i + 1; j < lista.length; j++) {
                combos.push(`${lista[i]}-${lista[j]}`);
            }
        }
        return combos;
    }

    const combinaciones = generarCombinaciones(conductores);

    function generarCampos() {
        const cantidad = parseInt(cableSetInput.value) || 0;
        contenedorResultados.innerHTML = "";
        bloqueResultados.style.display = cantidad > 0 ? "block" : "none";

        for (let i = 1; i <= cantidad; i++) {
            const tabla = document.createElement("table");
            tabla.classList.add("tabla-prueba");

            tabla.innerHTML = `
                <caption>Continuidad - Cable Set ${i}</caption>
                <tr>
                    <th>Punto</th>
                    <th>Resultado / N/A</th>
                    <th>Unidad</th>
                    <th>Observaciones</th>
                    <th>Imagen</th>
                </tr>`;

            combinaciones.forEach((punto) => {
                const fila = document.createElement("tr");
                const idResultado = `resultado_${i}_${punto}`;
                const idNA = `na_${i}_${punto}`;

                fila.innerHTML = `
                    <td>${punto}</td>
                    <td>
                        <div class="resultado-combinado">
                            <button type="button" class="na-btn" id="${idNA}">N/A</button>
                            <input type="text" name="${idResultado}" id="${idResultado}" />
                        </div>
                    </td>
                    <td><input name="unidad_${i}_${punto}" type="text" /></td>
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

                botonNA.addEventListener("click", () => {
                    if (inputResultado.disabled) {
                        inputResultado.disabled = false;
                        inputResultado.value = "";
                        botonNA.classList.remove("activo");
                    } else {
                        inputResultado.disabled = true;
                        inputResultado.value = "N/A";
                        botonNA.classList.add("activo");
                    }
                });

                const label = fila.querySelector("label");
                const inputFile = label.querySelector("input[type='file']");
                const textoAdjunto = label.querySelector(".adjunto-texto");

                inputFile.addEventListener("change", (e) => {
                    textoAdjunto.textContent = e.target.files[0] ? "📎 Archivo adjunto" : "";
                });
            });

            contenedorResultados.appendChild(tabla);
        }
    }

    // ✅ Eventos
    cableSetInput.addEventListener("input", generarCampos);
    generarCampos();

    document.getElementById("formulario-pruebas").addEventListener("submit", async function (e) {
        const tipo = document.getElementById("tipo-prueba")?.value;
        if (tipo !== "continuidad") return;

        e.preventDefault();

        const cableSets = parseInt(cableSetInput.value);
        if (!cableSets) {
            alert("Debe ingresar la cantidad de Cable Sets.");
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

        for (let i = 1; i <= cableSets; i++) {
            for (const punto of combinaciones) {
                const resultado = document.querySelector(`[name="resultado_${i}_${punto}"]`)?.value || "";
                const unidad = document.querySelector(`[name="unidad_${i}_${punto}"]`)?.value || "";
                const observaciones = document.querySelector(`[name="observaciones_${i}_${punto}"]`)?.value || "";
                const imagenInput = document.querySelector(`[name="imagen_${i}_${punto}"]`);
                const imagen = imagenInput?.files[0];

                datos.push({
                    cable_set: i,
                    punto_prueba: punto,
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
        formData.append("tipo_prueba", "continuidad");
        formData.append("cable_sets", cableSets);
        formData.append("tipo_alimentacion", tipo_alimentacion);
        formData.append("terminal", terminal);
        formData.append("datos", JSON.stringify(datos));
        imagenes.forEach((img) => formData.append("imagenes", img));

        const response = await fetch("/formulario/continuidad/guardar", {
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

window.initFormularioContinuidad = initFormularioContinuidad;

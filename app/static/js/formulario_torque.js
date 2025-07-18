function initFormularioTorque(tipoAlimentacion) {
    const cableSetInput = document.getElementById("cable_sets");
    const contenedorResultados = document.getElementById("contenedor-resultados");
    const bloqueResultados = document.getElementById("bloque-resultados");

    // ✅ Torque usa conductores unitarios, no combinaciones
    const conductores = tipoAlimentacion === "monofasica"
        ? ["L", "N", "PE"]
        : ["L1", "L2", "L3", "N", "PE"];

    function generarCampos() {
        const cantidad = parseInt(cableSetInput.value) || 0;
        contenedorResultados.innerHTML = "";
        bloqueResultados.style.display = cantidad > 0 ? "block" : "none";

        for (let i = 1; i <= cantidad; i++) {
            const tabla = document.createElement("table");
            tabla.classList.add("tabla-prueba");

            tabla.innerHTML = `
                <caption>Torque - Cable Set ${i}</caption>
                <tr>
                    <th>Conductor</th>
                    <th>Valor Nominal</th>
                    <th>Valor Comprobación</th>
                    <th>Unidad</th>
                    <th>Observaciones</th>
                    <th>Imagen</th>
                </tr>`;

            conductores.forEach((conductor) => {
                const fila = document.createElement("tr");
                const idNominal = `nominal_${i}_${conductor}`;
                const idComprobacion = `comprobacion_${i}_${conductor}`;

                fila.innerHTML = `
                    <td>${conductor}</td>
                    <td><input name="${idNominal}" type="text" /></td>
                    <td><input name="${idComprobacion}" type="text" /></td>
                    <td><input name="unidad_${i}_${conductor}" type="text" /></td>
                    <td><input name="observaciones_${i}_${conductor}" type="text" /></td>
                    <td>
                        <label class="camera-label">
                            📷 <span class="adjunto-texto"></span>
                            <input type="file" accept="image/*" name="imagen_${i}_${conductor}" style="display:none;" />
                        </label>
                    </td>
                `;
                tabla.appendChild(fila);

                const label = fila.querySelector("label");
                const inputFile = label.querySelector("input[type='file']");
                const textoAdjunto = label.querySelector(".adjunto-texto");

                inputFile.addEventListener("change", () => {
                    textoAdjunto.textContent = inputFile.files.length ? "📎 Archivo adjunto" : "";
                });
            });

            contenedorResultados.appendChild(tabla);
        }
    }

    cableSetInput.addEventListener("input", generarCampos);
    generarCampos();

    document.getElementById("formulario-pruebas").addEventListener("submit", async function (e) {
        const tipo = document.getElementById("tipo-prueba")?.value;
        if (tipo !== "torque") return;

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
            for (const conductor of conductores) {
                const nominal = document.querySelector(`[name="nominal_${i}_${conductor}"]`)?.value || "";
                const comprobacion = document.querySelector(`[name="comprobacion_${i}_${conductor}"]`)?.value || "";
                const unidad = document.querySelector(`[name="unidad_${i}_${conductor}"]`)?.value || "";
                const observaciones = document.querySelector(`[name="observaciones_${i}_${conductor}"]`)?.value || "";
                const imagenInput = document.querySelector(`[name="imagen_${i}_${conductor}"]`);
                const imagen = imagenInput?.files[0];

                datos.push({
                    cable_set: i,
                    punto_prueba: conductor,
                    valor_nominal: nominal,
                    valor_comprobacion: comprobacion,
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
        formData.append("tipo_prueba", "torque");
        formData.append("cable_sets", cableSets);
        formData.append("tipo_alimentacion", tipo_alimentacion);
        formData.append("terminal", terminal);
        formData.append("datos", JSON.stringify(datos));
        imagenes.forEach((img) => formData.append("imagenes", img));

        const response = await fetch("/formulario/torque/guardar", {
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

window.initFormularioTorque = initFormularioTorque;

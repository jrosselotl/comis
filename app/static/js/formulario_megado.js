function initFormularioMegado(tipoAlimentacion) {
    const cableSetInput = document.getElementById("cable_sets");
    const referenciaComunInput = document.getElementById("referencia-comun");
    const tiempoInputGlobal = document.getElementById("tiempo-aplicado-global");
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
        const referenciaComun = referenciaComunInput.value;
        const tiempoGlobal = tiempoInputGlobal.value;
        contenedorResultados.innerHTML = "";
        bloqueResultados.style.display = cantidad > 0 ? "block" : "none";

        for (let i = 1; i <= cantidad; i++) {
            const tabla = document.createElement("table");
            tabla.classList.add("tabla-prueba");

            tabla.innerHTML = `
                <caption>Megado - Cable Set ${i}</caption>
                <tr>
                    <th>Punto</th>
                    <th>Referencia</th>
                    <th>Resultado</th>
                    <th>Tiempo</th>
                    <th>¿Aprobado?</th>
                    <th>Observaciones</th>
                    <th>Imagen</th>
                </tr>`;

            combinaciones.forEach((punto, idx) => {
                const fila = document.createElement("tr");
                fila.innerHTML = `
                    <td>${punto}</td>
                    <td><input name="referencia_${i}_${punto}" type="text" value="${referenciaComun}" readonly /></td>
                    <td><input name="resultado_${i}_${punto}" type="text" /></td>
                    <td><input name="tiempo_${i}_${punto}" type="text" value="${tiempoGlobal}" readonly /></td>
                    <td><input name="aprobado_${i}_${punto}" type="checkbox" /></td>
                    <td><input name="observaciones_${i}_${punto}" type="text" /></td>
                    <td>
                        <label class="camera-label">
                            📷 <span class="adjunto-texto"></span>
                            <input type="file" accept="image/*" name="imagen_${i}_${punto}" style="display:none;" />
                        </label>
                    </td>
                `;
                tabla.appendChild(fila);

                const label = fila.querySelector("label");
                const inputFile = label.querySelector("input[type='file']");
                const textoAdjunto = label.querySelector(".adjunto-texto");

                inputFile.addEventListener("change", (e) => {
                    textoAdjunto.textContent = e.target.files.length > 0 ? "📎 Archivo adjunto" : "";
                });
            });

            contenedorResultados.appendChild(tabla);
        }
    }

    cableSetInput.addEventListener("input", generarCampos);
    referenciaComunInput.addEventListener("input", generarCampos);
    tiempoInputGlobal.addEventListener("input", generarCampos);
    generarCampos();

    // Mostrar campo tiempo si se elige Megado
    document.getElementById("campo-tiempo-aplicado").style.display = "block";

    // SUBMIT
    document.getElementById("formulario-pruebas").addEventListener("submit", async function (e) {
        const tipo_prueba_valor = document.getElementById("tipo-prueba")?.value;
        if (tipo_prueba_valor !== "megado") return;

        e.preventDefault();

        const cableSets = parseInt(cableSetInput.value);
        const referenciaComun = referenciaComunInput.value;
        const tiempoGlobal = tiempoInputGlobal.value;

        const datos = [];
        const imagenes = [];

        // Obtener campos del nombre del equipo
        const proyecto_id = document.getElementById("proyecto_id").value;
        const ubicacion_1 = document.getElementById("ubicacion_1").value;
        const numero_ubicacion_1 = document.getElementById("numero_ubicacion_1").value;
        const ubicacion_2 = document.getElementById("ubicacion_2")?.value || "";
        const numero_ubicacion_2 = document.getElementById("numero_ubicacion_2")?.value || "";
        const tipo_equipo = document.getElementById("tipo_equipo").value;
        const numero_tipo_equipo = document.getElementById("numero_tipo_equipo").value;
        const sub_equipo = document.getElementById("sub_equipo")?.value || "";
        const numero_sub_equipo = document.getElementById("numero_sub_equipo")?.value || "";

        let partes = [`${proyecto_id}`, `${ubicacion_1}${numero_ubicacion_1}`];
        if (ubicacion_1 === "COLO" && ubicacion_2 && numero_ubicacion_2) {
            partes.push(`${ubicacion_2}${numero_ubicacion_2}`);
        }
        partes.push(`${tipo_equipo}${numero_tipo_equipo}`);
        if (sub_equipo && numero_sub_equipo) {
            partes.push(`${sub_equipo}${numero_sub_equipo}`);
        }
        const codigo_equipo = partes.join("-");

        for (let i = 1; i <= cableSets; i++) {
            for (const punto of combinaciones) {
                const resultado = document.querySelector(`[name="resultado_${i}_${punto}"]`)?.value || "";
                const aprobado = document.querySelector(`[name="aprobado_${i}_${punto}"]`)?.checked || false;
                const observaciones = document.querySelector(`[name="observaciones_${i}_${punto}"]`)?.value || "";
                const imagenInput = document.querySelector(`[name="imagen_${i}_${punto}"]`);
                const imagen = imagenInput?.files[0];

                datos.push({
                    cable_set: i,
                    punto_prueba: punto,
                    referencia_valor: referenciaComun,
                    resultado_valor: resultado,
                    tiempo_aplicado: tiempoGlobal,
                    aprobado: aprobado,
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
        formData.append("tipo_prueba", "megado");
        formData.append("cable_sets", cableSets);
        formData.append("datos", JSON.stringify(datos));
        imagenes.forEach(img => formData.append("imagenes", img));

        const response = await fetch("/formulario/guardar", {
            method: "POST",
            body: formData
        });

        const res = await response.json().catch(() => alert("Error interno del servidor"));
        alert(res?.mensaje || "Error al guardar");
    });
}

window.initFormularioMegado = initFormularioMegado;

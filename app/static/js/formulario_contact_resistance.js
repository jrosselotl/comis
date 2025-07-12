function initFormularioContactResistance(tipoAlimentacion) {
    const cableSetInput = document.getElementById("cable_sets");
    const referenciaComunInput = document.getElementById("referencia-comun");
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
                    <th>Resultado</th>
                    <th>¿Aprobado?</th>
                    <th>Observaciones</th>
                    <th>Imagen</th>
                </tr>`;

            combinaciones.forEach((punto) => {
                const fila = document.createElement("tr");
                fila.innerHTML = `
                    <td>${punto}</td>
                    <td><input name="referencia_${i}_${punto}" type="text" value="${referenciaComun}" readonly /></td>
                    <td><input name="resultado_${i}_${punto}" type="text" /></td>
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
                const resultadoInput = fila.querySelector(`input[name="resultado_${i}_${punto}"]`);

                inputFile.addEventListener("change", async (e) => {
                    const file = e.target.files[0];
                    if (file) {
                        textoAdjunto.textContent = "📎 Archivo adjunto";

                        const reader = new FileReader();
                        reader.onload = async () => {
                            try {
                                const { data: { text } } = await Tesseract.recognize(reader.result, 'eng');
                                const match = text.match(/[\d]+(?:[\.,]\d+)?\s?(?:kV|KV|\u03a9|ohm|M\u03a9|G\u03a9|V|mA|A)?/);
                                if (match) {
                                    resultadoInput.value = match[0].replace(",", ".").trim();
                                } else {
                                    resultadoInput.value = text.trim();
                                }
                            } catch (err) {
                                console.error("Error OCR:", err);
                            }
                        };
                        reader.readAsDataURL(file);
                    } else {
                        textoAdjunto.textContent = "";
                    }
                });
            });

            contenedorResultados.appendChild(tabla);
        }
    }

    cableSetInput.addEventListener("input", generarCampos);
    referenciaComunInput.addEventListener("input", generarCampos);
    generarCampos();

    document.getElementById("formulario-pruebas").addEventListener("submit", async function (e) {
        const tipo = document.getElementById("tipo-prueba")?.value;
        if (tipo !== "contact_resistance") return;

        e.preventDefault();

        const cableSets = parseInt(cableSetInput.value);
        const referenciaComun = referenciaComunInput.value;

        if (!cableSets || !referenciaComun) {
            alert("Debe ingresar Cable Sets y un Valor de Referencia.");
            return;
        }

        const datos = [];
        const imagenes = [];

        const proyectoSelect = document.getElementById("proyecto_id");
        const proyecto_id = proyectoSelect.value;

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
                const aprobado = document.querySelector(`[name="aprobado_${i}_${punto}"]`)?.checked || false;
                const observaciones = document.querySelector(`[name="observaciones_${i}_${punto}"]`)?.value || "";
                const imagenInput = document.querySelector(`[name="imagen_${i}_${punto}"]`);
                const imagen = imagenInput?.files[0];

                datos.push({
                    cable_set: i,
                    punto_prueba: punto,
                    referencia_valor: referenciaComun,
                    resultado_valor: resultado,
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
        formData.append("tipo_prueba", "contact_resistance");
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

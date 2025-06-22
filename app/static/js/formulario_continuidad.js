document.addEventListener("DOMContentLoaded", function () {
    const cableSetInput = document.getElementById("cable-set");
    const referenciaComunInput = document.getElementById("referencia-comun");
    const contenedorResultados = document.getElementById("contenedor-resultados");
    const pruebas = ["L1", "L2", "L3", "N", "E"];

    function generarCampos() {
        const cantidad = parseInt(cableSetInput.value) || 0;
        const referenciaComun = referenciaComunInput.value;
        contenedorResultados.innerHTML = "";

        for (let i = 1; i <= cantidad; i++) {
            const tabla = document.createElement("table");
            tabla.classList.add("tabla-prueba");

            const caption = document.createElement("caption");
            caption.textContent = `Continuidad - Cable Set ${i}`;
            tabla.appendChild(caption);

            const encabezado = document.createElement("tr");
            encabezado.innerHTML = `
                <th>Punto</th>
                <th>Referencia</th>
                <th>Resultado</th>
                <th>¿Aprobado?</th>
                <th>Observaciones</th>
                <th>Imagen</th>`;
            tabla.appendChild(encabezado);

            pruebas.forEach((punto) => {
                const fila = document.createElement("tr");
                fila.innerHTML = `
                    <td>${punto}</td>
                    <td><input name="referencia_${i}_${punto}" type="text" value="${referenciaComun}" readonly /></td>
                    <td><input name="resultado_${i}_${punto}" type="text" /></td>
                    <td><input name="aprobado_${i}_${punto}" type="checkbox" /></td>
                    <td><input name="observaciones_${i}_${punto}" type="text" /></td>
                    <td></td>`;

                const label = document.createElement("label");
                label.classList.add("camera-label");
                label.innerHTML = `📷 <span class="adjunto-texto"></span>
                    <input type="file" accept="image/*" capture="environment" name="imagen_${i}_${punto}" style="display: none;">`;
                fila.querySelector("td:last-child").appendChild(label);

                label.querySelector("input").addEventListener("change", (e) => {
                    label.querySelector(".adjunto-texto").textContent = e.target.files.length > 0 ? "📎 Archivo adjunto" : "";
                });

                tabla.appendChild(fila);
            });

            contenedorResultados.appendChild(tabla);
        }
    }

    cableSetInput.addEventListener("input", generarCampos);
    referenciaComunInput.addEventListener("input", generarCampos);
    generarCampos();  // inicial

    document.getElementById("formulario-pruebas").addEventListener("submit", async function (e) {
        e.preventDefault();

        const cableSets = parseInt(cableSetInput.value);
        const codigoEquipo = document.getElementById("codigo-equipo").value;
        const tipoEquipo = document.getElementById("tipo-equipo").value;
        const colo = document.getElementById("colo").value;
        const ce = document.getElementById("ce").value;
        const proyectoId = document.getElementById("proyecto-id").value;
        const referenciaComun = referenciaComunInput.value;

        const datos = [];
        const imagenes = [];

        for (let i = 1; i <= cableSets; i++) {
            for (const punto of pruebas) {
                const resultado = document.querySelector(`[name="resultado_${i}_${punto}"]`).value;
                const aprobado = document.querySelector(`[name="aprobado_${i}_${punto}"]`).checked;
                const observaciones = document.querySelector(`[name="observaciones_${i}_${punto}"]`).value;
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
        formData.append("proyecto_id", proyectoId);
        formData.append("codigo_equipo", `${colo}-${ce}-${codigoEquipo}`);
        formData.append("tipo", tipoEquipo);
        formData.append("tipo_prueba", "continuidad");
        formData.append("cable_sets", cableSets);
        formData.append("datos", JSON.stringify(datos));
        imagenes.forEach(img => formData.append("imagenes", img));

        const response = await fetch("/formulario/guardar", {
            method: "POST",
            body: formData
        });

        const res = await response.json();
        alert(res.mensaje || "Error al guardar");
    });
});

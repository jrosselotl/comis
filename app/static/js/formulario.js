<script>
document.getElementById("formulario-pruebas").addEventListener("submit", async function (e) {
    e.preventDefault();

    const tipoPrueba = document.getElementById("tipo-prueba").value;
    const cableSets = parseInt(document.getElementById("cable-set").value);
    const proyectoId = document.getElementById("proyecto-id").value;
    const codigoEquipo = document.getElementById("codigo-equipo").value;
    const tipoEquipo = document.getElementById("tipo-equipo").value;
    const colo = document.getElementById("colo").value;
    const ce = document.getElementById("ce").value;

    const pruebasContinuidad = ["L1", "L2", "L3", "N", "E"];
    const pruebasMegado = ["L1-L2", "L1-L3", "L2-L3", "L1-N", "L2-N", "L3-N", "L1-E", "L2-E", "L3-E", "N-E"];
    const pruebas = tipoPrueba === "continuidad" ? pruebasContinuidad : pruebasMegado;

    const datos = [];
    const imagenes = [];

    for (let i = 1; i <= cableSets; i++) {
        for (const punto of pruebas) {
            const referencia = document.querySelector(`[name="referencia_${i}_${punto}"]`).value;
            const resultado = document.querySelector(`[name="resultado_${i}_${punto}"]`).value;
            const tiempo = document.querySelector(`[name="tiempo_${i}_${punto}"]`)?.value || "";
            const observaciones = document.querySelector(`[name="observaciones_${i}_${punto}"]`)?.value || "";
            const aprobado = document.querySelector(`[name="aprobado_${i}_${punto}"]`).checked;
            const imagenInput = document.querySelector(`[name="imagen_${i}_${punto}"]`);

            const imagen = imagenInput?.files[0];
            if (imagen) {
                imagenes.push(imagen);
            } else {
                imagenes.push(new File([], ""));
            }

            datos.push({
                cable_set: i,
                punto_prueba: punto,
                referencia_valor: referencia,
                resultado_valor: resultado,
                tiempo_aplicado: tiempo,
                aprobado: aprobado,
                observaciones: observaciones
            });
        }
    }

    const formData = new FormData();
    formData.append("proyecto_id", proyectoId);
    formData.append("codigo_equipo", `${colo}-${ce}-${codigoEquipo}`);
    formData.append("tipo", tipoEquipo);
    formData.append("tipo_prueba", tipoPrueba);
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
</script>

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("parametrosForm");
    const tabla = document.getElementById("tablaParametros").querySelector("tbody");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const datos = Object.fromEntries(formData.entries());

        const endpoint = `/parametros/${datos.tipo_test}/crear`;

        const body = {
            proyecto_id: 1, // se puede automatizar si hay selección por proyecto
            codigo_equipo: `${datos.ubicacion_1}-${datos.ubicacion_2}-${datos.tipo_equipo}-${datos.sub_equipo}`,
            valor_minimo: parseFloat(datos.valor_minimo),
            valor_maximo: parseFloat(datos.valor_maximo),
            unidad: datos.unidad,
            voltaje_requerido: parseFloat(datos.voltaje_requerido),
            observaciones: datos.observaciones
        };

        try {
            const res = await fetch(endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body)
            });

            if (!res.ok) throw new Error("Error al guardar parámetro");

            const data = await res.json();
            agregarFila(data);
            form.reset();
        } catch (err) {
            alert(err.message);
        }
    });

    function agregarFila(p) {
        const fila = document.createElement("tr");
        fila.innerHTML = `
            <td>${p.codigo_equipo.split("-")[0]}</td>
            <td>${p.codigo_equipo.split("-")[1]}</td>
            <td>${p.codigo_equipo.split("-")[2]}</td>
            <td>${p.codigo_equipo.split("-")[3]}</td>
            <td>${p.valor_minimo}</td>
            <td>${p.valor_maximo}</td>
            <td>${p.unidad}</td>
            <td>${p.voltaje_requerido}</td>
            <td>${p.observaciones}</td>
            <td><button class="editar">Editar</button> <button class="eliminar">Eliminar</button></td>
        `;
        tabla.appendChild(fila);
    }
});

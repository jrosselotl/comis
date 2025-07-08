document.addEventListener("DOMContentLoaded", async function () {
    const form = document.getElementById("parametros-form");
    const tabla = document.querySelector("#tabla-parametros tbody");
    const testSelect = document.getElementById("test");

    // Listar al cargar
    await cargarParametros();

    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        const datos = Object.fromEntries(new FormData(form).entries());

        const endpoint = `/parametros/${datos.test}/crear`;
        const body = {
            proyecto_id: 1,
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
            if (!res.ok) throw new Error("Error al guardar");

            await cargarParametros();
            form.reset();
        } catch (err) {
            alert(err.message);
        }
    });

    async function cargarParametros() {
        const tipo_test = testSelect.value;
        const res = await fetch(`/parametros/${tipo_test}/listar`);
        const datos = await res.json();
        tabla.innerHTML = "";
        datos.forEach(p => agregarFila(p, tipo_test));
    }

    function agregarFila(p, tipo_test) {
        const fila = document.createElement("tr");
        const [u1, u2, tipo, sub] = p.codigo_equipo.split("-");
        fila.innerHTML = `
            <td>${u1}</td>
            <td>${u2}</td>
            <td>${tipo}</td>
            <td>${sub}</td>
            <td>${p.valor_minimo}</td>
            <td>${p.valor_maximo}</td>
            <td>${p.unidad}</td>
            <td>${p.voltaje_requerido}</td>
            <td>${p.observaciones}</td>
            <td>
                <button onclick="editarParametro(${p.id}, '${tipo_test}')">Editar</button>
                <button onclick="eliminarParametro(${p.id}, '${tipo_test}')">Eliminar</button>
            </td>
        `;
        tabla.appendChild(fila);
    }

    window.editarParametro = async function (id, tipo_test) {
        const nuevo_valor = prompt("Nueva observación:");
        if (!nuevo_valor) return;

        await fetch(`/parametros/${tipo_test}/${id}/editar`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ observaciones: nuevo_valor })
        });

        await cargarParametros();
    };

    window.eliminarParametro = async function (id, tipo_test) {
        if (!confirm("¿Eliminar parámetro?")) return;
        await fetch(`/parametros/${tipo_test}/${id}/eliminar`, { method: "DELETE" });
        await cargarParametros();
    };

    testSelect.addEventListener("change", cargarParametros);
});

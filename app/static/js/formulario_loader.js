document.addEventListener("DOMContentLoaded", async function () {
    // Cargar lista de proyectos
    const select = document.getElementById("proyecto_id");
    try {
        const res = await fetch("/proyectos/");
        const data = await res.json();
        select.innerHTML = "";
        data.forEach(p => {
            const opt = document.createElement("option");
            opt.value = p.id;
            opt.textContent = p.nombre;
            select.appendChild(opt);
        });
    } catch {
        select.innerHTML = `<option value="">Error cargando proyectos</option>`;
    }

    // Visibilidad condicional
    const ubicacion1 = document.getElementById("ubicacion_1");
    const labelUbicacion2 = document.getElementById("label-ubicacion_2");
    const tipoEquipo = document.getElementById("tipo_equipo");
    const labelSubEquipo = document.getElementById("label-sub_equipo");

    function actualizarVisibilidadCampos() {
        if (ubicacion1.value === "COLO") {
            labelUbicacion2.style.display = "block";
        } else {
            labelUbicacion2.style.display = "none";
        }

        if (["PDU", "MSB"].includes(tipoEquipo.value)) {
            labelSubEquipo.style.display = "block";
        } else {
            labelSubEquipo.style.display = "none";
        }
    }

    ubicacion1.addEventListener("change", actualizarVisibilidadCampos);
    tipoEquipo.addEventListener("change", actualizarVisibilidadCampos);
    actualizarVisibilidadCampos(); // Ejecutar al inicio por si hay valores cargados

    // Manejo de scripts por tipo de prueba
    const tipoPruebaSelect = document.getElementById("tipo-prueba");
    const tipoAlimentacionSelect = document.getElementById("tipo_alimentacion");
    const cableSetsInput = document.getElementById("cable_sets");
    const contenedorResultados = document.getElementById("contenedor-resultados");
    let currentScript;

    const scriptMap = {
        continuidad: "/static/js/formulario_continuidad.js",
        megado: "/static/js/formulario_megado.js"
    };

    async function loadScript() {
        const tipo = tipoPruebaSelect.value;
        const tipoAlimentacion = tipoAlimentacionSelect.value;

        if (!tipo || !scriptMap[tipo]) {
            contenedorResultados.innerHTML = "";
            return;
        }

        if (currentScript) currentScript.remove();

        currentScript = document.createElement("script");
        currentScript.src = scriptMap[tipo];
        currentScript.onload = () => {
            const initFunctionName = `initFormulario${tipo.charAt(0).toUpperCase()}${tipo.slice(1)}`;
            const initFunction = window[initFunctionName];
            if (typeof initFunction === "function") {
                initFunction(tipoAlimentacion);
            } else {
                console.error(`Función ${initFunctionName} no encontrada.`);
            }
        };
        document.body.appendChild(currentScript);
    }

    tipoPruebaSelect.addEventListener("change", loadScript);
    tipoAlimentacionSelect.addEventListener("change", loadScript);
    cableSetsInput.addEventListener("input", loadScript);

    if (tipoPruebaSelect.value) {
        await loadScript();
    }
});

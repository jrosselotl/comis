document.addEventListener("DOMContentLoaded", async function () {
    const selectProyecto = document.getElementById("proyecto_id");
    const tipoPruebaSelect = document.getElementById("tipo-prueba");
    const tipoAlimentacionSelect = document.getElementById("tipo_alimentacion");
    const contenedorResultados = document.getElementById("contenedor-resultados");

    // 1. Cargar lista de proyectos
    try {
        const res = await fetch("/proyectos/");
        const data = await res.json();
        selectProyecto.innerHTML = "";
        data.forEach(p => {
            const opt = document.createElement("option");
            opt.value = p.id;
            opt.textContent = p.nombre;
            selectProyecto.appendChild(opt);
        });
    } catch {
        selectProyecto.innerHTML = `<option value="">Error cargando proyectos</option>`;
    }

    // 2. Mapa de scripts por tipo de prueba
    const scriptMap = {
        continuidad: "/static/js/formulario_continuidad.js",
        megado: "/static/js/formulario_megado.js"
    };

    let currentScript = null;

    async function loadTipoPruebaScript() {
        const tipo = tipoPruebaSelect.value;

        if (!tipo || !scriptMap[tipo]) {
            contenedorResultados.innerHTML = "";
            return;
        }

        if (currentScript) {
            currentScript.remove();
        }

        currentScript = document.createElement("script");
        currentScript.src = scriptMap[tipo];
        currentScript.onload = () => {
            const tipoAlimentacion = tipoAlimentacionSelect.value;
            const initFunctionName = `initFormulario${tipo.charAt(0).toUpperCase()}${tipo.slice(1)}`;
            const initFunction = window[initFunctionName];
            if (typeof initFunction === "function") {
                initFunction(tipoAlimentacion);
            } else {
                console.error(`No se encontró la función ${initFunctionName}`);
            }
        };
        document.body.appendChild(currentScript);
    }

    // 3. Disparadores
    tipoPruebaSelect.addEventListener("change", loadTipoPruebaScript);
    tipoAlimentacionSelect.addEventListener("change", loadTipoPruebaScript);

    if (tipoPruebaSelect.value) {
        await loadTipoPruebaScript();
    }
});

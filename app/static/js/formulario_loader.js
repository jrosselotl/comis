document.addEventListener("DOMContentLoaded", async function () {
    const proyectoSelect = document.getElementById("proyecto_id");
    const tipoPruebaSelect = document.getElementById("tipo-prueba");
    const tipoAlimentacionSelect = document.getElementById("tipo_alimentacion");
    const cableSetsInput = document.getElementById("cable_sets");
    const contenedorResultados = document.getElementById("contenedor-resultados");
    let currentScript;

    const scriptMap = {
        continuidad: "/static/js/formulario_continuidad.js",
        megado: "/static/js/formulario_megado.js",
        contact_resistance: "/static/js/formulario_contact_resistance.js",
        torque: "/static/js/formulario_torque.js"
    };

    async function cargarProyectos() {
        try {
            const res = await fetch("/proyectos/");
            const data = await res.json();
            proyectoSelect.innerHTML = "";
            data.forEach(p => {
                const opt = document.createElement("option");
                opt.value = p.id;
                opt.textContent = p.nombre;
                proyectoSelect.appendChild(opt);
            });

            if (data.length > 0) {
                proyectoSelect.value = data[0].id;
                await cargarTestsPorProyecto(data[0].id);
            }
        } catch {
            proyectoSelect.innerHTML = `<option value="">Error cargando proyectos</option>`;
        }
    }

    async function cargarTestsPorProyecto(proyectoId) {
        try {
            const res = await fetch(`/proyectos/${proyectoId}/tests`);
            const data = await res.json();
            tipoPruebaSelect.innerHTML = "";

            data.forEach(test => {
                const opt = document.createElement("option");
                opt.value = test.nombre;
                opt.textContent = test.nombre.charAt(0).toUpperCase() + test.nombre.slice(1).replace("_", " ");
                tipoPruebaSelect.appendChild(opt);
            });

            await loadScript();  // Cargar el script al cambiar proyecto
        } catch {
            tipoPruebaSelect.innerHTML = `<option value="">Error cargando tests</option>`;
        }
    }

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
            const initFunctionName = `initFormulario${tipo
                .split("_")
                .map(p => p.charAt(0).toUpperCase() + p.slice(1))
                .join("")}`;
            const initFunction = window[initFunctionName];
            if (typeof initFunction === "function") {
                initFunction(tipoAlimentacion);
            } else {
                console.error(`Función ${initFunctionName} no encontrada.`);
            }
        };
        document.body.appendChild(currentScript);
    }

    // Eventos
    proyectoSelect.addEventListener("change", async () => {
        await cargarTestsPorProyecto(proyectoSelect.value);
    });

    tipoPruebaSelect.addEventListener("change", loadScript);
    tipoAlimentacionSelect.addEventListener("change", loadScript);
    cableSetsInput.addEventListener("input", loadScript);

    // Iniciar
    await cargarProyectos();

    // Mostrar/ocultar campos condicionales
    const ubicacion1 = document.getElementById("ubicacion_1");
    const tipoEquipo = document.getElementById("tipo_equipo");
    const labelUbicacion2 = document.getElementById("label-ubicacion_2");
    const labelSubEquipo = document.getElementById("label-sub_equipo");

    function actualizarVisibilidadCampos() {
        if (ubicacion1 && labelUbicacion2) {
            labelUbicacion2.style.display = ubicacion1.value === "COLO" ? "block" : "none";
        }
        if (tipoEquipo && labelSubEquipo) {
            labelSubEquipo.style.display = ["PDU", "MSB"].includes(tipoEquipo.value) ? "block" : "none";
        }
    }

    if (ubicacion1) ubicacion1.addEventListener("change", actualizarVisibilidadCampos);
    if (tipoEquipo) tipoEquipo.addEventListener("change", actualizarVisibilidadCampos);
    actualizarVisibilidadCampos();

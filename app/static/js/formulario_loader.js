document.addEventListener("DOMContentLoaded", async function () {
    const proyectoSelect = document.getElementById("proyecto_id");
    const tipoPruebaSelect = document.getElementById("tipo-prueba");
    const tipoAlimentacionSelect = document.getElementById("tipo_alimentacion");
    const cableSetsInput = document.getElementById("cable_sets");
    const contenedorResultados = document.getElementById("contenedor-resultados");
    const unidadLabel = document.getElementById("label-unidad");
    const unidadSelect = document.getElementById("unidad");
    let currentScript;

    const scriptMap = {
        continuidad: "/static/js/formulario_continuidad.js",
        megado: "/static/js/formulario_megado.js",
        contact_resistance: "/static/js/formulario_contact_resistance.js",
        torque: "/static/js/formulario_torque.js"
    };

    async function cargarTestsPorProyecto(proyectoId) {
        try {
            const res = await fetch(`/proyectos/${proyectoId}/tests`);
            const data = await res.json();

            tipoPruebaSelect.innerHTML = "";

            const defaultOption = document.createElement("option");
            defaultOption.value = "";
            defaultOption.textContent = "Seleccione prueba...";
            defaultOption.disabled = true;
            defaultOption.selected = true;
            tipoPruebaSelect.appendChild(defaultOption);

            data.forEach(test => {
                const opt = document.createElement("option");
                opt.value = test.nombre;
                opt.setAttribute("data-id", test.id);
                opt.textContent = test.nombre.charAt(0).toUpperCase() + test.nombre.slice(1).replace("_", " ");
                tipoPruebaSelect.appendChild(opt);
            });

            await loadScript();
        } catch {
            tipoPruebaSelect.innerHTML = `<option value="">Error cargando tests</option>`;
        }
    }

    async function loadScript() {
        const tipo = tipoPruebaSelect.value;
        const tipoAlimentacion = tipoAlimentacionSelect.value;

        actualizarUnidades(tipo);

        if (!tipo || !scriptMap[tipo]) {
            contenedorResultados.innerHTML = "";
            document.getElementById("bloque-caracteristicas").style.display = "none";
            return;
        }

        if (currentScript) {
            currentScript.remove();
            currentScript = null;
        }

        currentScript = document.createElement("script");
        currentScript.src = scriptMap[tipo];
        currentScript.onload = () => {
    setTimeout(() => {
        const initFunctionName = `initFormulario${tipo
            .split("_")
            .map(p => p.charAt(0).toUpperCase() + p.slice(1))
            .join("")}`;
        const initFunction = window[initFunctionName];
        if (typeof initFunction === "function") {
            initFunction(tipoAlimentacion);

            // 🟢 Forzar generación de campos si ya hay cable sets definidos
            const cableSetInput = document.getElementById("cable_sets");
            if (cableSetInput && cableSetInput.value) {
                cableSetInput.dispatchEvent(new Event("input"));
            }
        } else {
            console.error(`Función ${initFunctionName} no encontrada.`);
        }
    }, 50); // ligera espera para asegurar que el DOM esté listo
};

        document.body.appendChild(currentScript);
        document.getElementById("bloque-caracteristicas").style.display = "block";
    }

    function actualizarUnidades(tipoPrueba) {
        if (!window.UNIDADES_POR_TEST) {
            console.warn("UNIDADES_POR_TEST no está definido.");
            unidadLabel.style.display = "none";
            return;
        }

        const unidades = window.UNIDADES_POR_TEST[tipoPrueba] || [];
        unidadSelect.innerHTML = `<option value="">Seleccione unidad...</option>`;

        unidades.forEach(u => {
            const opt = document.createElement("option");
            opt.value = u;
            opt.textContent = u;
            unidadSelect.appendChild(opt);
        });

        unidadLabel.style.display = unidades.length > 0 ? "block" : "none";
    }

    async function cargarProyectos() {
        try {
            const res = await fetch("/proyectos/");
            const proyectos = await res.json();

            proyectoSelect.innerHTML = "";
            const defaultOption = document.createElement("option");
            defaultOption.value = "";
            defaultOption.textContent = "Seleccione proyecto...";
            defaultOption.disabled = true;
            defaultOption.selected = true;
            proyectoSelect.appendChild(defaultOption);

            proyectos.forEach(p => {
                const opt = document.createElement("option");
                opt.value = p.id;
                opt.textContent = p.nombre;
                proyectoSelect.appendChild(opt);
            });
        } catch {
            proyectoSelect.innerHTML = `<option value="">Error cargando proyectos</option>`;
        }
    }

    proyectoSelect.addEventListener("change", async () => {
        await cargarTestsPorProyecto(proyectoSelect.value);
    });

    tipoPruebaSelect.addEventListener("change", loadScript);
    tipoAlimentacionSelect.addEventListener("change", loadScript);
    cableSetsInput.addEventListener("input", loadScript);

    await cargarProyectos();

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
});

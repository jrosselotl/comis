document.addEventListener("DOMContentLoaded", async function () {
    // Cargar lista de proyectos
    const select = document.getElementById("proyecto_id"); // corregido id (era proyecto-id)
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

    // Manejadores de prueba
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

document.addEventListener("DOMContentLoaded", function () {
  const ubicacion1 = document.getElementById("ubicacion_1");
  const labelUbicacion2 = document.getElementById("label-ubicacion_2");

  const tipoEquipo = document.getElementById("tipo_equipo");
  const labelSubEquipo = document.getElementById("label-sub_equipo");

  ubicacion1.addEventListener("change", () => {
    if (ubicacion1.value === "COLO") {
      labelUbicacion2.style.display = "block";
    } else {
      labelUbicacion2.style.display = "none";
    }
  });

  tipoEquipo.addEventListener("change", () => {
    const valor = tipoEquipo.value;
    if (valor === "PDU" || valor === "MSB") {
      labelSubEquipo.style.display = "block";
    } else {
      labelSubEquipo.style.display = "none";
    }
  });
});


    // Ejecutar al cargar por si vienen valores por defecto
    actualizarVisibilidadCampos();

    // Asociar eventos
    ubicacion1.addEventListener("change", actualizarVisibilidadCampos);
    tipoEquipo.addEventListener("change", actualizarVisibilidadCampos);
});

// static/js/cargar_formulario.js

document.addEventListener("DOMContentLoaded", () => {
  const tipoPruebaSelect = document.getElementById("tipo-prueba");
  const unidadSelect = document.getElementById("unidad");
  const referenciaInput = document.getElementById("referencia-comun");
  const tiempoField = document.getElementById("campo-tiempo-aplicado");
  const caracteristicas = document.getElementById("bloque-caracteristicas");
  const resultados = document.getElementById("bloque-resultados");
  const tipoAlimentacionSelect = document.getElementById("tipo_alimentacion");

  // ✅ Cargar proyectos y tipos de test
  async function cargarProyectosYTipos() {
    try {
      const [proyectosRes, tiposRes] = await Promise.all([
        fetch("/proyectos/listar"),
        fetch("/tests/listar"),
      ]);
      const proyectos = await proyectosRes.json();
      const tipos = await tiposRes.json();

      // Llenar proyectos
      const proyectoSelect = document.getElementById("proyecto_id");
      proyectoSelect.innerHTML = "<option value=''>Seleccione...</option>";
      proyectos.forEach((p) => {
        const opt = document.createElement("option");
        opt.value = p.id;
        opt.textContent = p.nombre;
        proyectoSelect.appendChild(opt);
      });

      // Llenar tipos de test
      tipoPruebaSelect.innerHTML = "<option value=''>Seleccione prueba...</option>";
      tipos.forEach((t) => {
        const opt = document.createElement("option");
        opt.value = t.nombre;
        opt.textContent = t.nombre.charAt(0).toUpperCase() + t.nombre.slice(1);
        tipoPruebaSelect.appendChild(opt);
      });
    } catch (error) {
      console.error("Error cargando proyectos y tipos:", error);
    }
  }

  // ✅ Actualizar unidades según test
  function actualizarUnidadesPorTest(test) {
    unidadSelect.innerHTML = "<option value=''>Seleccione unidad...</option>";

    if (window.UNIDADES_POR_TEST && window.UNIDADES_POR_TEST[test]) {
      window.UNIDADES_POR_TEST[test].forEach((u) => {
        const opt = document.createElement("option");
        opt.value = u;
        opt.textContent = u;
        unidadSelect.appendChild(opt);
      });
      document.getElementById("label-unidad").style.display = "block";
    } else {
      document.getElementById("label-unidad").style.display = "none";
    }
  }

  // ✅ Evento al cambiar tipo de prueba
  tipoPruebaSelect.addEventListener("change", () => {
    const tipo = tipoPruebaSelect.value;

    // Mostrar u ocultar bloques
    caracteristicas.style.display = tipo ? "block" : "none";
    resultados.style.display = "none";

    // Limpiar campos comunes
    referenciaInput.value = "";
    actualizarUnidadesPorTest(tipo);
    tiempoField.style.display = tipo === "megado" ? "block" : "none";

    // Cargar el formulario dinámico según el test
    if (tipo === "continuidad") {
      initFormularioContinuidad(tipoAlimentacionSelect.value);
    }
    if (tipo === "megado") {
      initFormularioMegado(tipoAlimentacionSelect.value);
    }
    if (tipo === "contact_resistance") {
      initFormularioContactResistance(tipoAlimentacionSelect.value);
    }
    if (tipo === "torque") {
      initFormularioTorque(tipoAlimentacionSelect.value);
    }
  });

  // ✅ Cambiar tipo de alimentación reactiva los tests
  tipoAlimentacionSelect.addEventListener("change", () => {
    tipoPruebaSelect.dispatchEvent(new Event("change"));
  });

  // ✅ Mostrar u ocultar Ubicación secundaria
  document.getElementById("ubicacion_1").addEventListener("change", (e) => {
    const val = e.target.value;
    document.getElementById("label-ubicacion_2").style.display =
      val === "COLO" ? "block" : "none";
  });

  cargarProyectosYTipos();
});

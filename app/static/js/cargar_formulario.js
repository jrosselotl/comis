document.addEventListener("DOMContentLoaded", () => {
  const tipoPruebaSelect = document.getElementById("tipo-prueba");
  const unidadSelect = document.getElementById("unidad");
  const referenciaInput = document.getElementById("referencia-comun");
  const tiempoField = document.getElementById("campo-tiempo-aplicado");
  const caracteristicas = document.getElementById("bloque-caracteristicas");
  const resultados = document.getElementById("bloque-resultados");
  const tipoAlimentacionSelect = document.getElementById("tipo_alimentacion");

  async function cargarProyectosYTipos() {
    const [proyectosRes, tiposRes] = await Promise.all([
      fetch("/proyectos/listar"),
      fetch("/tests/listar"),
    ]);
    const proyectos = await proyectosRes.json();
    const tipos = await tiposRes.json();

    const proyectoSelect = document.getElementById("proyecto_id");
    proyectoSelect.innerHTML = "<option value=''>Seleccione...</option>";
    proyectos.forEach(p => {
      const opt = document.createElement("option");
      opt.value = p.id;
      opt.textContent = p.nombre;
      proyectoSelect.appendChild(opt);
    });

    tipoPruebaSelect.innerHTML = "<option value=''>Seleccione prueba...</option>";
    tipos.forEach(t => {
      const opt = document.createElement("option");
      opt.value = t.nombre;
      opt.textContent = t.nombre.charAt(0).toUpperCase() + t.nombre.slice(1);
      tipoPruebaSelect.appendChild(opt);
    });
  }

  tipoPruebaSelect.addEventListener("change", () => {
    const tipo = tipoPruebaSelect.value;
    caracteristicas.style.display = tipo ? "block" : "none";
    resultados.style.display = "none";

    unidadSelect.innerHTML = "<option value=''>Seleccione unidad...</option>";
    referenciaInput.value = "";
    tiempoField.style.display = tipo === "megado" ? "block" : "none";

    // Mostrar u ocultar scripts según tipo de prueba
    if (tipo === "continuidad") initFormularioContinuidad(tipoAlimentacionSelect.value);
    if (tipo === "megado") initFormularioMegado(tipoAlimentacionSelect.value);
    if (tipo === "contact_resistance") initFormularioContactResistance(tipoAlimentacionSelect.value);
    if (tipo === "torque") initFormularioTorque(tipoAlimentacionSelect.value);
  });

  tipoAlimentacionSelect.addEventListener("change", () => {
    tipoPruebaSelect.dispatchEvent(new Event("change"));
  });

  document.getElementById("ubicacion_1").addEventListener("change", (e) => {
    const val = e.target.value;
    document.getElementById("label-ubicacion_2").style.display = val === "COLO" ? "block" : "none";
  });

  document.getElementById("tipo_test").addEventListener("change", async function () {
      const tipo = this.value;
      const unidadSelect = document.getElementById("unidad-general");
  
      if (!tipo) {
          unidadSelect.innerHTML = "";
          return;
      }
  
      try {
          const resp = await fetch(`/tests/unidades?tipo_test=${tipo}`);
          const data = await resp.json();
  
          unidadSelect.innerHTML = "";
          data.unidades.forEach(u => {
              const option = document.createElement("option");
              option.value = u;
              option.textContent = u;
              unidadSelect.appendChild(option);
          });
      } catch (error) {
          console.error("Error cargando unidades:", error);
      }
  });

  cargarProyectosYTipos();
});

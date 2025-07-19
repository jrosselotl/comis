// static/js/cargar_formulario.js

document.addEventListener("DOMContentLoaded", () => {
  const tipoPruebaSelect = document.getElementById("tipo-prueba");
  const caracteristicas = document.getElementById("bloque-caracteristicas");
  const resultados = document.getElementById("bloque-resultados");
  const tipoAlimentacionSelect = document.getElementById("tipo_alimentacion");

  const ubicacion1Select = document.getElementById("ubicacion_1");
  const numeroUbicacion1Select = document.getElementById("numero_ubicacion_1");
  const ubicacion2Container = document.getElementById("label-ubicacion_2");
  const ubicacion2Select = document.getElementById("ubicacion_2");
  const numeroUbicacion2Select = document.getElementById("numero_ubicacion_2");

  const tipoEquipoSelect = document.getElementById("tipo_equipo");
  const numeroTipoEquipoSelect = document.getElementById("numero_tipo_equipo");
  const subEquipoContainer = document.getElementById("label-sub_equipo");
  const subEquipoSelect = document.getElementById("sub_equipo");
  const numeroSubEquipoSelect = document.getElementById("numero_sub_equipo");

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

      // Evento para cargar ubicaciones y equipos cuando cambia el proyecto
      proyectoSelect.addEventListener("change", () => {
        if (proyectoSelect.value) {
          cargarUbicaciones(proyectoSelect.value);
          cargarEquipos();
        }
      });
    } catch (error) {
      console.error("Error cargando proyectos y tipos:", error);
    }
  }

  // ✅ Cargar ubicaciones desde la BD
  async function cargarUbicaciones(proyectoId) {
    try {
      const res = await fetch(`/ubicaciones/listar?proyecto_id=${proyectoId}`);
      const ubicaciones = await res.json();

      // Poblar ubicacion_1
      ubicacion1Select.innerHTML = "<option value=''>Seleccione</option>";
      ubicaciones.forEach((u) => {
        const opt = document.createElement("option");
        opt.value = u.ubicacion_1;
        opt.textContent = u.ubicacion_1;
        opt.dataset.numeros = JSON.stringify(u.numero_ubicacion_1 || []);
        opt.dataset.ubicacion2 = u.ubicacion_2 || "";
        opt.dataset.numeros2 = JSON.stringify(u.numero_ubicacion_2 || []);
        ubicacion1Select.appendChild(opt);
      });

      ubicacion1Select.addEventListener("change", async () => {
        const selected = ubicacion1Select.selectedOptions[0];
        if (!selected) return;

        // Poblar número ubicación 1
        const numeros1 = JSON.parse(selected.dataset.numeros || "[]");
        numeroUbicacion1Select.innerHTML = "";
        numeros1.forEach((n) => {
          const opt = document.createElement("option");
          opt.value = n;
          opt.textContent = n;
          numeroUbicacion1Select.appendChild(opt);
        });

        // Mostrar / ocultar ubicación 2
        const ubicacion2 = selected.dataset.ubicacion2;
        if (ubicacion2) {
          ubicacion2Container.style.display = "block";
          ubicacion2Select.innerHTML = `<option value="${ubicacion2}">${ubicacion2}</option>`;
          const numeros2 = JSON.parse(selected.dataset.numeros2 || "[]");
          numeroUbicacion2Select.innerHTML = "";
          numeros2.forEach((n) => {
            const opt = document.createElement("option");
            opt.value = n;
            opt.textContent = n;
            numeroUbicacion2Select.appendChild(opt);
          });
        } else {
          ubicacion2Container.style.display = "none";
          ubicacion2Select.innerHTML = "";
          numeroUbicacion2Select.innerHTML = "";
        }
      });
    } catch (error) {
      console.error("Error cargando ubicaciones:", error);
    }
  }

  // ✅ Cargar tipos de equipos desde la BD
  async function cargarEquipos() {
    try {
      const res = await fetch(`/tipo_equipos/listar`);
      const equipos = await res.json();

      tipoEquipoSelect.innerHTML = "<option value=''>Seleccione</option>";
      equipos.forEach((e) => {
        const opt = document.createElement("option");
        opt.value = e.tipo_equipo;
        opt.textContent = e.tipo_equipo;
        opt.dataset.numeros = JSON.stringify(e.numero_tipo_equipo || []);
        opt.dataset.sub = e.sub_equipo || "";
        opt.dataset.numerosSub = JSON.stringify(e.numero_sub_equipo || []);
        tipoEquipoSelect.appendChild(opt);
      });

      tipoEquipoSelect.addEventListener("change", () => {
        const selected = tipoEquipoSelect.selectedOptions[0];
        if (!selected) return;

        // Poblar número tipo equipo
        const numeros = JSON.parse(selected.dataset.numeros || "[]");
        numeroTipoEquipoSelect.innerHTML = "";
        numeros.forEach((n) => {
          const opt = document.createElement("option");
          opt.value = n;
          opt.textContent = n;
          numeroTipoEquipoSelect.appendChild(opt);
        });

        // Mostrar / ocultar subequipo
        const sub = selected.dataset.sub;
        if (sub) {
          subEquipoContainer.style.display = "block";
          subEquipoSelect.innerHTML = `<option value="${sub}">${sub}</option>`;
          const numerosSub = JSON.parse(selected.dataset.numerosSub || "[]");
          numeroSubEquipoSelect.innerHTML = "";
          numerosSub.forEach((n) => {
            const opt = document.createElement("option");
            opt.value = n;
            opt.textContent = n;
            numeroSubEquipoSelect.appendChild(opt);
          });
        } else {
          subEquipoContainer.style.display = "none";
          subEquipoSelect.innerHTML = "";
          numeroSubEquipoSelect.innerHTML = "";
        }
      });
    } catch (error) {
      console.error("Error cargando equipos:", error);
    }
  }

  // ✅ Evento al cambiar tipo de prueba
  tipoPruebaSelect.addEventListener("change", async () => {
    const tipo = tipoPruebaSelect.value;

    caracteristicas.style.display = tipo ? "block" : "none";
    resultados.style.display = "none";
     // ✅ Llenar unidades dinámicamente desde el backend
  if (tipo) {
    try {
      const res = await fetch(`/tests/unidades?tipo_test=${tipo}`);
      const data = await res.json();

      const unidadSelect = document.getElementById("unidad");
      const labelUnidad = document.getElementById("label-unidad");
      unidadSelect.innerHTML = "<option value=''>Seleccione unidad...</option>";

      if (data.unidades && data.unidades.length > 0) {
        data.unidades.forEach((u) => {
          const opt = document.createElement("option");
          opt.value = u;
          opt.textContent = u;
          unidadSelect.appendChild(opt);
        });
        labelUnidad.style.display = "block";
      } else {
        labelUnidad.style.display = "none";
      }
    } catch (error) {
      console.error("Error cargando unidades:", error);
    }
  }
    
    if (tipo === "continuidad") initFormularioContinuidad(tipoAlimentacionSelect.value);
    if (tipo === "megado") initFormularioMegado(tipoAlimentacionSelect.value);
    if (tipo === "contact_resistance") initFormularioContactResistance(tipoAlimentacionSelect.value);
    if (tipo === "torque") initFormularioTorque(tipoAlimentacionSelect.value);
  });

  // ✅ Cambiar tipo de alimentación reactiva los tests
  tipoAlimentacionSelect.addEventListener("change", () => {
    tipoPruebaSelect.dispatchEvent(new Event("change"));
  });

  cargarProyectosYTipos();
});

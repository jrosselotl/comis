document.addEventListener("DOMContentLoaded", () => {
  const btnDashboard = document.getElementById("btn-dashboard");
  const btnMyTests = document.getElementById("btn-mytests");
  const btnNewTest = document.getElementById("btn-newtest");

  const sectionDashboard = document.getElementById("section-dashboard");
  const sectionMyTests = document.getElementById("section-mytests");
  const sectionNewTest = document.getElementById("section-newtest");

  const tablaMyTests = document.getElementById("tabla-mytests");
  const graficoCanvas = document.getElementById("grafico-tests");

  // ✅ Mostrar solo una sección
  function sectionShow(section) {
    [sectionDashboard, sectionMyTests, sectionNewTest].forEach((s) =>
      s.classList.add("hidden")
    );
    seccion.classList.remove("hidden");
  }

  // ✅ Cargar gráfico dinámico desde backend
  async function cargarGrafico() {
    if (!graficoCanvas) return;

    try {
      const res = await fetch("/test_realizados/estadisticas_usuario/1"); // Usuario logueado (mock id=1)
      const datos = await res.json();

      const tipos = Object.keys(datos);
      const cantidades = Object.values(datos);

      new Chart(graficoCanvas, {
        type: "bar",
        data: {
          labels: tipos,
          datasets: [
            {
              label: "Tests realizados",
              data: cantidades,
              backgroundColor: ["#3498db", "#9b59b6", "#e67e22", "#27ae60"],
            },
          ],
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
        },
      });
    } catch (error) {
      console.error("Error cargando estadísticas:", error);
    }
  }

  // ✅ Cargar My Tests dinámico desde backend
  async function cargarMyTests() {
    tablaMyTests.innerHTML = "";
    try {
      const res = await fetch("/test_realizados/listar_usuario/1"); // Usuario logueado (mock id=1)
      const tests = await res.json();

      tests.forEach((t) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${t.id}</td>
          <td>${t.tipo_prueba}</td>
          <td>${t.equipo}</td>
          <td>${new Date(t.fecha).toLocaleDateString()}</td>
          <td>${t.estado}</td>
          <td>
            ${
              t.estado === "Incompleto"
                ? `<button class="btn btn-continuar" data-id="${t.id}">Continuar</button>`
                : ""
            }
            ${
              t.estado === "Completo"
                ? `<button class="btn btn-enviar" data-id="${t.id}">Enviar</button>`
                : ""
            }
          </td>
        `;
        tablaMyTests.appendChild(tr);
      });

      // ✅ Eventos para botones
      document.querySelectorAll(".btn-continuar").forEach((btn) => {
        btn.addEventListener("click", async (e) => {
          const id = e.target.dataset.id;
          alert(`Cargar formulario para continuar test ID ${id}...`);
          // TODO: Cargar datos en el formulario según test_id
          mostrarSeccion(sectionNewTest);
        });
      });

      document.querySelectorAll(".btn-enviar").forEach((btn) => {
        btn.addEventListener("click", async (e) => {
          const id = e.target.dataset.id;
          if (
            confirm(`¿Deseas enviar el PDF por correo para el test ID ${id}?`)
          ) {
            const resp = await fetch(`/test_realizados/enviar_pdf/${id}`, {
              method: "POST",
            });
            const data = await resp.json();
            alert(data.mensaje || "PDF enviado correctamente.");
          }
        });
      });
    } catch (error) {
      console.error("Error cargando mis tests:", error);
    }
  }

  // ✅ Eventos Sidebar
  btnDashboard.addEventListener("click", () => {
    mostrarSeccion(sectionDashboard);
    cargarGrafico();
  });

  btnMyTests.addEventListener("click", () => {
    mostrarSeccion(sectionMyTests);
    cargarMyTests();
  });

  btnNewTest.addEventListener("click", () => {
    mostrarSeccion(sectionNewTest);
  });

  // ✅ Mostrar Dashboard al inicio
  mostrarSeccion(sectionDashboard);
  cargarGrafico();
});

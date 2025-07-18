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
  function mostrarSeccion(seccion) {
    [sectionDashboard, sectionMyTests, sectionNewTest].forEach((s) => {
      s.classList.add("hidden");
    });
    seccion.classList.remove("hidden");
  }

  // ✅ Cargar gráfico (por ahora datos mock)
  function cargarGrafico() {
    if (!graficoCanvas) return;

    // Datos falsos por ahora, luego llamaremos al backend /tests/estadisticas
    const tipos = ["Continuidad", "Megado", "Contact Resistance", "Torque"];
    const cantidades = [5, 3, 7, 2];

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
        plugins: {
          legend: { display: false },
        },
      },
    });
  }

  // ✅ Cargar My Tests (por ahora datos mock)
  function cargarMyTests() {
    tablaMyTests.innerHTML = ""; // limpiar tabla

    // Datos de ejemplo, luego lo haremos dinámico desde /tests/listar_usuario
    const tests = [
      { id: 1, tipo: "continuidad", equipo: "COLO1-PDU01", fecha: "2025-07-18", estado: "Incompleto" },
      { id: 2, tipo: "megado", equipo: "COLO1-MSB01", fecha: "2025-07-17", estado: "Completo" },
      { id: 3, tipo: "torque", equipo: "WTP2-LBP01", fecha: "2025-07-15", estado: "Enviado" },
    ];

    tests.forEach((t) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${t.id}</td>
        <td>${t.tipo}</td>
        <td>${t.equipo}</td>
        <td>${t.fecha}</td>
        <td>${t.estado}</td>
        <td>
          ${t.estado === "Incompleto" ? `<button class="btn btn-continuar" data-id="${t.id}">Continuar</button>` : ""}
          ${t.estado === "Completo" ? `<button class="btn btn-enviar" data-id="${t.id}">Enviar</button>` : ""}
        </td>
      `;
      tablaMyTests.appendChild(tr);
    });

    // ✅ Eventos para botones
    document.querySelectorAll(".btn-continuar").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const id = e.target.dataset.id;
        alert(`Cargar formulario para continuar test ID ${id}...`);
        // Aquí se debería cargar el formulario con los datos existentes
        mostrarSeccion(sectionNewTest);
      });
    });

    document.querySelectorAll(".btn-enviar").forEach((btn) => {
      btn.addEventListener("click", async (e) => {
        const id = e.target.dataset.id;
        if (confirm(`¿Deseas enviar el PDF por correo para el test ID ${id}?`)) {
          alert(`(Mock) Enviando PDF para test ID ${id}...`);
          // Luego haremos fetch(`/tests/enviar_pdf/${id}`, { method: "POST" })
        }
      });
    });
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

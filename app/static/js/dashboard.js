document.addEventListener("DOMContentLoaded", () => {
  const btnDashboard = document.getElementById("btnDashboard");
  const btnMyTest = document.getElementById("btnMyTest");
  const btnNewTest = document.getElementById("btnNewTest");

  const sectionDashboard = document.getElementById("section-dashboard");
  const sectionMyTest = document.getElementById("section-mytest");
  const sectionNewTest = document.getElementById("section-newtest");

  const tableMyTest = document.getElementById("table-mytest");
  const chartCanvas = document.getElementById("chart-test");
  let chartInstance = null;

  const sidebar = document.getElementById("sidebar");
  const hamburger = document.getElementById("hamburger");

  // ✅ Mostrar solo una sección
  function showSection(section) {
    [sectionDashboard, sectionMyTest, sectionNewTest].forEach((s) =>
      s.classList.add("hidden")
    );
    section.classList.remove("hidden");
  }

  // ✅ Cargar el gráfico dinámico (con base actual)
  async function loadChart() {
  if (!chartCanvas) return;

  try {
    const res = await fetch("/test_performed/list_user/1");
    const tests = await res.json();

    // ✅ Agrupamos por test_type
    const stats = {};
    tests.forEach((t) => {
      const type = t.test_type || t.name;
      stats[type] = (stats[type] || 0) + 1;
    });

    const types = Object.keys(stats);      // → ["continuity", "torque", ...]
    const quantities = Object.values(stats); // → [5, 2, ...]

    if (chartInstance) chartInstance.destroy();

    chartInstance = new Chart(chartCanvas, {
      type: "bar",
      data: {
        labels: types.map((t) => t.charAt(0).toUpperCase() + t.slice(1)), // ✅ Bonito en X
        datasets: [
          {
            label: "Completed Tests",
            data: quantities,
            backgroundColor: [
              "rgba(52, 152, 219, 0.8)",
              "rgba(155, 89, 182, 0.8)",
              "rgba(230, 126, 34, 0.8)",
              "rgba(39, 174, 96, 0.8)"
            ],
            borderRadius: 8
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (context) => `Total: ${context.raw}`
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { stepSize: 1, color: "#2c3e50" }
          },
          x: { ticks: { color: "#2c3e50" } }
        }
      }
    });
  } catch (error) {
    console.error("Error loading stats:", error);
  }
}


  // ✅ Cargar lista de tests (sin tocar nada)
  async function loadMyTest() {
    tableMyTest.innerHTML = "";
    try {
      const res = await fetch("/test_performed/list_user/1");
      const tests = await res.json();

      tests.forEach((t) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${t.asset}</td>
          <td>${t.test_type || t.name}</td>
          <td>${new Date(t.date).toLocaleDateString()}</td>
          <td>${t.status}</td>
          <td>
            ${
              t.status === "Incomplete"
                ? `<button class="btn btn-continue" data-id="${t.id}">✏️ Edit</button>`
                : `<button class="btn btn-send" data-id="${t.id}">📧 Send</button>`
            }
          </td>
        `;
        tableMyTest.appendChild(tr);
      });

      // ✅ Evento Editar
      document.querySelectorAll(".btn-continue").forEach((btn) => {
        btn.addEventListener("click", async (e) => {
          const id = e.target.dataset.id;
          console.log(`🔄 Cargando datos para test ID ${id}...`);

          try {
            const res = await fetch(`/form/load_test/${id}`);
            if (!res.ok) throw new Error("No se pudo cargar el test");
            const testData = await res.json();

            if (typeof window.loadExistingTest === "function") {
              window.loadExistingTest(testData);
            } else {
              alert("⚠️ Falta implementar la función loadExistingTest en tu JS de formularios.");
            }

            showSection(sectionNewTest);
          } catch (err) {
            console.error("Error cargando datos del test:", err);
            alert("Error cargando datos del test.");
          }
        });
      });

      // ✅ Evento Enviar PDF
      document.querySelectorAll(".btn-send").forEach((btn) => {
        btn.addEventListener("click", async (e) => {
          const id = e.target.dataset.id;
          if (confirm(`Do you want to send the PDF by email for test ID ${id}?`)) {
            const resp = await fetch(`/test_done/send_pdf/${id}`, {
              method: "POST"
            });
            const data = await resp.json();
            alert(data.message || "PDF sent successfully.");
          }
        });
      });
    } catch (error) {
      console.error("Error loading my tests:", error);
    }
  }

  // ✅ Eventos Sidebar
  btnDashboard.addEventListener("click", () => {
    showSection(sectionDashboard);
    loadChart();
  });

  btnMyTest.addEventListener("click", () => {
    showSection(sectionMyTest);
    loadMyTest();
  });

  btnNewTest.addEventListener("click", () => {
    showSection(sectionNewTest);
  });

  // ✅ Hamburguesa (Mobile)
  hamburger.addEventListener("click", () => {
    sidebar.style.display = sidebar.style.display === "block" ? "none" : "block";
  });

  // ✅ Inicio
  showSection(sectionDashboard);
  loadChart();
});

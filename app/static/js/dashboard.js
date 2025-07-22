document.addEventListener("DOMContentLoaded", () => {
  const btnDashboard = document.getElementById("btnDashboard");
  const btnMyTest = document.getElementById("btnMyTest");
  const btnNewTest = document.getElementById("btnNewTest");

  const sectionDashboard = document.getElementById("section-dashboard");
  const sectionMyTest = document.getElementById("section-mytest");
  const sectionNewTest = document.getElementById("section-newtest");

  const tableMyTest = document.getElementById("table-mytest");
  const chartCanvas = document.getElementById("chart-test");
  let chartInstance = null; // 🔹 Para evitar superponer gráficos

  // ✅ Mostrar solo una sección
  function showSection(section) {
    [sectionDashboard, sectionMyTest, sectionNewTest].forEach((s) =>
      s.classList.add("hidden")
    );
    section.classList.remove("hidden");
  }

  // ✅ Cargar el gráfico dinámico
  async function loadChart() {
    if (!chartCanvas) return;

    try {
      const res = await fetch("/test_performed/list_user/1");
      const data = await res.json();

      const types = Object.keys(data);
      const quantities = Object.values(data);

      // Evitar que se superpongan varios gráficos
      if (chartInstance) {
        chartInstance.destroy();
      }

      chartInstance = new Chart(chartCanvas, {
        type: "bar",
        data: {
          labels: types,
          datasets: [
            {
              label: "Completed Tests",
              data: quantities,
              backgroundColor: [
                "rgba(52, 152, 219, 0.8)",  // Azul
                "rgba(155, 89, 182, 0.8)",  // Morado
                "rgba(230, 126, 34, 0.8)",  // Naranja
                "rgba(39, 174, 96, 0.8)"    // Verde
              ],
              borderRadius: 8
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (context) => `Total: ${context.raw}`
              }
            },
            datalabels: { // ✅ Muestra los números encima de cada barra
              anchor: "end",
              align: "top",
              color: "#2c3e50",
              font: { weight: "bold" },
              formatter: (value) => value
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1,
                color: "#2c3e50",
              }
            },
            x: {
              ticks: { color: "#2c3e50" }
            }
          }
        },
        plugins: [ChartDataLabels]
      });
    } catch (error) {
      console.error("Error loading stats:", error);
    }
  }

  // ✅ Cargar lista de tests
  async function loadMyTest() {
    tableMyTest.innerHTML = "";
    try {
      const res = await fetch("/test_performed/list_user/1");
      const tests = await res.json();

      tests.forEach((t) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${t.asset}</td>
          <td>${t.test_type}</td>
          <td>${new Date(t.date).toLocaleDateString()}</td>
          <td>${t.status}</td>
          <td>
            ${
              t.status === "Incomplete"
                ? `<button class="btn btn-continue" data-id="${t.id}">✏️ Edit</button>`
                : ""
            }
            ${
              t.status !== "Sent"
                ? `<button class="btn btn-send" data-id="${t.id}">📧 Send</button>`
                : ""
            }
          </td>
        `;
        tableMyTest.appendChild(tr);
      });

      // ✅ Eventos botones
      document.querySelectorAll(".btn-continue").forEach((btn) => {
        btn.addEventListener("click", async (e) => {
          const id = e.target.dataset.id;
          alert(`Loading form to continue test ID ${id}...`);
          showSection(sectionNewTest);
        });
      });

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

  // ✅ Mostrar Dashboard al inicio
  showSection(sectionDashboard);
  loadChart();
});

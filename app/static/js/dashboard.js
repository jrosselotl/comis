document.addEventListener("DOMContentLoaded", () => {
  const btnDashboard = document.getElementById("btn-dashboard");
  const btnMyTest = document.getElementById("btn-mytest");
  const btnNewTest = document.getElementById("btn-newtest");

  const sectionDashboard = document.getElementById("section-dashboard");
  const sectionMyTest = document.getElementById("section-mytest");
  const sectionNewTest = document.getElementById("section-newtest");

  const tableMyTest = document.getElementById("tabla-mytest");
  const chartCanvas = document.getElementById("grafico-test");

  // ✅ Show only one section
  function showSection(section) {
    [sectionDashboard, sectionMyTest, sectionNewTest].forEach((s) =>
      s.classList.add("hidden")
    );
    section.classList.remove("hidden");
  }

  // ✅ Load dynamic chart from backend
  async function loadChart() {
    if (!chartCanvas) return;

    try {
      const res = await fetch("/test_done/user_stats/1"); // Logged user (mock id=1)
      const data = await res.json();

      const types = Object.keys(data);
      const quantities = Object.values(data);

      new Chart(chartCanvas, {
        type: "bar",
        data: {
          labels: types,
          datasets: [
            {
              label: "Completed Test",
              data: quantities,
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
      console.error("Error loading stats:", error);
    }
  }

  // ✅ Load My Test dynamically from backend
  async function loadMyTest() {
    tableMyTest.innerHTML = "";
    try {
      const res = await fetch("/test_done/list_user/1"); // Logged user (mock id=1)
      const test = await res.json();

      test.forEach((t) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${t.id}</td>
          <td>${t.test_type}</td>
          <td>${t.equipment}</td>
          <td>${new Date(t.date).toLocaleDateString()}</td>
          <td>${t.status}</td>
          <td>
            ${
              t.status === "Incomplete"
                ? `<button class="btn btn-continue" data-id="${t.id}">Continue</button>`
                : ""
            }
            ${
              t.status === "Complete"
                ? `<button class="btn btn-send" data-id="${t.id}">Send</button>`
                : ""
            }
          </td>
        `;
        tableMyTests.appendChild(tr);
      });

      // ✅ Events for buttons
      document.querySelectorAll(".btn-continue").forEach((btn) => {
        btn.addEventListener("click", async (e) => {
          const id = e.target.dataset.id;
          alert(`Loading form to continue test ID ${id}...`);
          // TODO: Load data into the form by test_id
          showSection(sectionNewTest);
        });
      });

      document.querySelectorAll(".btn-send").forEach((btn) => {
        btn.addEventListener("click", async (e) => {
          const id = e.target.dataset.id;
          if (
            confirm(`Do you want to send the PDF by email for test ID ${id}?`)
          ) {
            const resp = await fetch(`/test_done/send_pdf/${id}`, {
              method: "POST",
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

  // ✅ Sidebar events
  btnDashboard.addEventListener("click", () => {
    showSection(sectionDashboard);
    loadChart();
  });

  btnMyTests.addEventListener("click", () => {
    showSection(sectionMyTests);
    loadMyTests();
  });

  btnNewTest.addEventListener("click", () => {
    showSection(sectionNewTest);
  });

  // ✅ Show Dashboard on start
  showSection(sectionDashboard);
  loadChart();
});

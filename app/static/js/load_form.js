document.addEventListener("DOMContentLoaded", () => {
  const location1Select = document.getElementById("location_1");
  const numberLocation1Select = document.getElementById("number_location_1");
  const location2Container = document.getElementById("label-location_2");
  const location2Select = document.getElementById("location_2");
  const numberLocation2Select = document.getElementById("number_location_2");

  const equipmentTypeSelect = document.getElementById("equipment_type");
  const numberEquipmentTypeSelect = document.getElementById("number_equipment_type");
  const subEquipmentContainer = document.getElementById("label-sub_equipment");
  const subEquipmentSelect = document.getElementById("sub_equipment");
  const numberSubEquipmentSelect = document.getElementById("number_sub_equipment");

  const testTypeSelect = document.getElementById("test-type");
  const featureBlock = document.getElementById("block-features");
  const resultBlock = document.getElementById("result-block");
  const powerTypeSelect = document.getElementById("power_type");

  // ✅ Helper para mostrar/ocultar selects con required
  function toggleSelectVisibility(select, show) {
    if (show) {
      select.parentElement.style.display = "block";
      select.required = true;
    } else {
      select.parentElement.style.display = "none";
      select.required = false;
      select.innerHTML = "";
    }
  }

  // ✅ Load project and test types
  async function loadLocation(projectId) {
  try {
    const res = await fetch(`/location/list?project_id=${projectId}`);
    const locationData = await res.json();

    // ✅ SOLO reiniciamos los campos secundarios
    location1Select.innerHTML = "<option value=''>Select</option>";
    location1Select.parentElement.style.display = "block"; // 🔥 SIEMPRE visible

    location2Container.style.display = "none";
    toggleSelectVisibility(numberLocation1Select, false);
    toggleSelectVisibility(numberLocation2Select, false);

    locationData.forEach((l) => {
      const opt = document.createElement("option");
      opt.value = l.location_1;
      opt.textContent = l.location_1;
      opt.dataset.number = JSON.stringify(l.number_location_1 || []);
      opt.dataset.location2 = l.location_2 || "";
      opt.dataset.number2 = JSON.stringify(l.number_location_2 || []);
      location1Select.appendChild(opt);
    });

    location1Select.addEventListener("change", () => {
      const selected = location1Select.selectedOptions[0];
      if (!selected) return;

      const numbers1 = JSON.parse(selected.dataset.number || "[]");
      const location2 = selected.dataset.location2;
      const numbers2 = JSON.parse(selected.dataset.number2 || []);

      // ✅ Reglas según tus casos
      toggleSelectVisibility(numberLocation1Select, numbers1.length > 0);

      if (location2) {
        location2Container.style.display = "block";
        location2Select.innerHTML = `<option value="${location2}">${location2}</option>`;
        toggleSelectVisibility(numberLocation2Select, numbers2.length > 0);
        if (numbers2.length > 0) {
          numberLocation2Select.innerHTML = "";
          numbers2.forEach((n) => {
            const opt = document.createElement("option");
            opt.value = n;
            opt.textContent = n;
            numberLocation2Select.appendChild(opt);
          });
        }
      } else {
        location2Container.style.display = "none";
        toggleSelectVisibility(numberLocation2Select, false);
      }
    });
  } catch (error) {
    console.error("Error loading location:", error);
  }
}


  // ✅ Load locations (con reglas específicas)
  async function loadLocation(projectId) {
    try {
      const res = await fetch(`/location/list?project_id=${projectId}`);
      const locationData = await res.json();

      // 🔥 Reset inicial
      location1Select.innerHTML = "<option value=''>Select</option>";
      toggleSelectVisibility(numberLocation1Select, false);
      location2Container.style.display = "none";
      toggleSelectVisibility(numberLocation2Select, false);

      locationData.forEach((l) => {
        const opt = document.createElement("option");
        opt.value = l.location_1;
        opt.textContent = l.location_1;
        opt.dataset.number = JSON.stringify(l.number_location_1 || []);
        opt.dataset.location2 = l.location_2 || "";
        opt.dataset.number2 = JSON.stringify(l.number_location_2 || []);
        location1Select.appendChild(opt);
      });

      location1Select.addEventListener("change", () => {
        const selected = location1Select.selectedOptions[0];
        if (!selected) return;

        const numbers1 = JSON.parse(selected.dataset.number || "[]");
        const location2 = selected.dataset.location2;
        const numbers2 = JSON.parse(selected.dataset.number2 || "[]");

        // --- Location 1 number
        if (numbers1.length > 0) {
          toggleSelectVisibility(numberLocation1Select, true);
          numberLocation1Select.innerHTML = "";
          numbers1.forEach((n) => {
            const opt = document.createElement("option");
            opt.value = n;
            opt.textContent = n;
            numberLocation1Select.appendChild(opt);
          });
        } else {
          toggleSelectVisibility(numberLocation1Select, false);
        }

        // --- Location 2
        if (location2) {
          location2Container.style.display = "block";
          location2Select.innerHTML = `<option value="${location2}">${location2}</option>`;
          if (numbers2.length > 0) {
            toggleSelectVisibility(numberLocation2Select, true);
            numberLocation2Select.innerHTML = "";
            numbers2.forEach((n) => {
              const opt = document.createElement("option");
              opt.value = n;
              opt.textContent = n;
              numberLocation2Select.appendChild(opt);
            });
          } else {
            toggleSelectVisibility(numberLocation2Select, false);
          }
        } else {
          location2Container.style.display = "none";
          toggleSelectVisibility(numberLocation2Select, false);
        }
      });
    } catch (error) {
      console.error("Error loading location:", error);
    }
  }

  // ✅ Load equipment types (sin cambios, ya funcionaba bien)
  async function loadEquipment() {
    try {
      const res = await fetch(`/equipment_type/list`);
      const equipmentData = await res.json();

      equipmentTypeSelect.innerHTML = "<option value=''>Select</option>";
      toggleSelectVisibility(numberEquipmentTypeSelect, false);
      subEquipmentContainer.style.display = "none";
      toggleSelectVisibility(numberSubEquipmentSelect, false);

      equipmentData.forEach((e) => {
        const opt = document.createElement("option");
        opt.value = e.equipment_type;
        opt.textContent = e.equipment_type;
        opt.dataset.number = JSON.stringify(e.number_equipment_type || []);
        opt.dataset.sub = e.sub_equipment || "";
        opt.dataset.numberSub = JSON.stringify(e.number_sub_equipment || []);
        equipmentTypeSelect.appendChild(opt);
      });

      equipmentTypeSelect.addEventListener("change", () => {
        const selected = equipmentTypeSelect.selectedOptions[0];
        if (!selected) return;

        const numbers = JSON.parse(selected.dataset.number || "[]");
        if (numbers.length > 0) {
          toggleSelectVisibility(numberEquipmentTypeSelect, true);
          numberEquipmentTypeSelect.innerHTML = "";
          numbers.forEach((n) => {
            const opt = document.createElement("option");
            opt.value = n;
            opt.textContent = n;
            numberEquipmentTypeSelect.appendChild(opt);
          });
        } else {
          toggleSelectVisibility(numberEquipmentTypeSelect, false);
        }

        const sub = selected.dataset.sub;
        if (sub) {
          subEquipmentContainer.style.display = "block";
          subEquipmentSelect.innerHTML = `<option value="${sub}">${sub}</option>`;
          const numbersSub = JSON.parse(selected.dataset.numberSub || "[]");
          if (numbersSub.length > 0) {
            toggleSelectVisibility(numberSubEquipmentSelect, true);
            numberSubEquipmentSelect.innerHTML = "";
            numbersSub.forEach((n) => {
              const opt = document.createElement("option");
              opt.value = n;
              opt.textContent = n;
              numberSubEquipmentSelect.appendChild(opt);
            });
          } else {
            toggleSelectVisibility(numberSubEquipmentSelect, false);
          }
        } else {
          subEquipmentContainer.style.display = "none";
          toggleSelectVisibility(numberSubEquipmentSelect, false);
        }
      });
    } catch (error) {
      console.error("Error loading equipment:", error);
    }
  }

  // ✅ Change test type → USANDO unit_by_test.js
  testTypeSelect.addEventListener("change", () => {
    const type = testTypeSelect.value;
    featureBlock.style.display = type ? "block" : "none";
    resultBlock.style.display = "none";

    if (type) loadUnitByTest(type);

    if (type === "continuity") initFormContinuity(powerTypeSelect.value);
    if (type === "isolation") initFormIsolation(powerTypeSelect.value);
    if (type === "contact_resistance") initFormContactResistance(powerTypeSelect.value);
    if (type === "torque") initFormTorque(powerTypeSelect.value);
  });

  powerTypeSelect.addEventListener("change", () => {
    testTypeSelect.dispatchEvent(new Event("change"));
  });

  loadProjectAndTestType();
});

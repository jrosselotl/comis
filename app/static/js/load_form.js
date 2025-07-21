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
  const resultBlock = document.getElementById("block-results");
  const powerTypeSelect = document.getElementById("power_type");
  

  // ✅ Load project and test types
  async function loadProjectAndTestType() {
    try {
      const [projectRes, testRes] = await Promise.all([
        fetch("/project/list"),
        fetch("/test/list"),
      ]);
      const projectData = await projectRes.json();
      const testData = await testRes.json();

      const projectSelect = document.getElementById("project_id");
      projectSelect.innerHTML = "<option value=''>Select...</option>";
      projectData.forEach((p) => {
        const opt = document.createElement("option");
        opt.value = p.id;
        opt.textContent = p.name;
        projectSelect.appendChild(opt);
      });

      testTypeSelect.innerHTML = "<option value=''>Select test...</option>";
      testData.forEach((t) => {
        const opt = document.createElement("option");
        opt.value = t.name;
        opt.textContent = t.name.charAt(0).toUpperCase() + t.name.slice(1);
        testTypeSelect.appendChild(opt);
      });

      projectSelect.addEventListener("change", () => {
        if (projectSelect.value) {
          loadLocation(projectSelect.value);
          loadEquipment();
        }
      });
    } catch (error) {
      console.error("Error loading project and test types:", error);
    }
  }

  // ✅ Load locations
  async function loadLocation(projectId) {
    try {
      const res = await fetch(`/location/list?project_id=${projectId}`);
      const locationData = await res.json();

      location1Select.innerHTML = "<option value=''>Select</option>";
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

  if (numbers1.length > 0) {
    numberLocation1Select.parentElement.style.display = "block";
    numberLocation1Select.innerHTML = "";
    numbers1.forEach((n) => {
      const opt = document.createElement("option");
      opt.value = n;
      opt.textContent = n;
      numberLocation1Select.appendChild(opt);
    });
  } else {
    numberLocation1Select.parentElement.style.display = "none";
    numberLocation1Select.innerHTML = "";
  }

  const location2 = selected.dataset.location2;
  if (location2) {
    location2Container.style.display = "block";
    location2Select.innerHTML = `<option value="${location2}">${location2}</option>`;
    const numbers2 = JSON.parse(selected.dataset.number2 || "[]");
    numberLocation2Select.innerHTML = "";
    numbers2.forEach((n) => {
      const opt = document.createElement("option");
      opt.value = n;
      opt.textContent = n;
      numberLocation2Select.appendChild(opt);
    });
  } else {
    location2Container.style.display = "none";
    location2Select.innerHTML = "";
    numberLocation2Select.innerHTML = "";
  }
});
    } catch (error) {
      console.error("Error loading location:", error);
    }
  }

  // ✅ Load equipment types
  async function loadEquipment() {
    try {
      const res = await fetch(`/equipment_type/list`);
      const equipmentData = await res.json();

      equipmentTypeSelect.innerHTML = "<option value=''>Select</option>";
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
    numberEquipmentTypeSelect.parentElement.style.display = "block";
    numberEquipmentTypeSelect.innerHTML = "";
    numbers.forEach((n) => {
      const opt = document.createElement("option");
      opt.value = n;
      opt.textContent = n;
      numberEquipmentTypeSelect.appendChild(opt);
    });
  } else {
    numberEquipmentTypeSelect.parentElement.style.display = "none";
    numberEquipmentTypeSelect.innerHTML = "";
  }

  const sub = selected.dataset.sub;
  if (sub) {
    subEquipmentContainer.style.display = "block";
    subEquipmentSelect.innerHTML = `<option value="${sub}">${sub}</option>`;

    const numbersSub = JSON.parse(selected.dataset.numberSub || "[]");
    if (numbersSub.length > 0) {
      numberSubEquipmentSelect.parentElement.style.display = "block";
      numberSubEquipmentSelect.innerHTML = "";
      numbersSub.forEach((n) => {
        const opt = document.createElement("option");
        opt.value = n;
        opt.textContent = n;
        numberSubEquipmentSelect.appendChild(opt);
      });
    } else {
      numberSubEquipmentSelect.parentElement.style.display = "none";
      numberSubEquipmentSelect.innerHTML = "";
    }
  } else {
    subEquipmentContainer.style.display = "none";
    subEquipmentSelect.innerHTML = "";
    numberSubEquipmentSelect.parentElement.style.display = "none";
    numberSubEquipmentSelect.innerHTML = "";
  }
});

    } catch (error) {
      console.error("Error loading equipment:", error);
    }
  }

  // ✅ Change test type
  testTypeSelect.addEventListener("change", async () => {
    const type = testTypeSelect.value;

    featureBlock.style.display = type ? "block" : "none";
    resultBlock.style.display = "none";

    if (type) {
      try {
        const res = await fetch(`/test/unit?test_type=${type}`);
        const data = await res.json();

        const unitSelect = document.getElementById("unit");
        const labelUnit = document.getElementById("label-unit");
        unitSelect.innerHTML = "<option value=''>Select unit...</option>";

        if (data.unit && data.unit.length > 0) {
          data.unit.forEach((u) => {
            const opt = document.createElement("option");
            opt.value = u;
            opt.textContent = u;
            unitSelect.appendChild(opt);
          });
          labelUnit.style.display = "block";
        } else {
          labelUnit.style.display = "none";
        }
      } catch (error) {
        console.error("Error loading unit:", error);
      }
    }

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

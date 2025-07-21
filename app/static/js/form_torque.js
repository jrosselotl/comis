function initFormTorque(powerType) {
    const cableSetInput = document.getElementById("cable_sets");
    const selectedUnit = document.getElementById("unit")?.value || "";
    const resultContainer = document.getElementById("result-container");
    const resultBlock = document.getElementById("result-block");
    

    // ✅ Torque uses individual conductors, not combinations
    const conductors = powerType === "single_phase"
        ? ["L", "N", "PE"]
        : ["L1", "L2", "L3", "N", "PE"];

    function generateFields() {
        const quantity = parseInt(cableSetInput.value) || 0;
        resultContainer.innerHTML = "";
        resultBlock.style.display = quantity > 0 ? "block" : "none";

        // ✅ Load global unit select (only once)
        if (window.UNIT_BY_TEST && window.UNIT_BY_TEST["torque"]) {
            const unitSelect = document.getElementById("unit");
            const labelUnit = document.getElementById("label-unit");

            if (unitSelect && labelUnit) {
                unitSelect.innerHTML = '<option value="">Select unit...</option>';
                window.UNIT_BY_TEST["torque"].forEach((u) => {
                    const opt = document.createElement("option");
                    opt.value = u;
                    opt.textContent = u;
                    unitSelect.appendChild(opt);
                });
                labelUnit.style.display = "block";
            }
        }

        for (let i = 1; i <= quantity; i++) {
            const table = document.createElement("table");
            table.classList.add("test-table");

            table.innerHTML = `
                <caption>Torque - Cable Set ${i}</caption>
                <tr>
                    <th>Conductor</th>
                    <th>Nominal Value</th>
                    <th>Verification Value</th>
                    <th>Unit</th>
                    <th>Observation</th>
                    <th>Image</th>
                </tr>`;

            conductors.forEach((conductor) => {
                const row = document.createElement("tr");
                const idNominal = `nominal_${i}_${conductor}`;
                const idVerification = `verification_${i}_${conductor}`;

                row.innerHTML = `
                    <td>${conductor}</td>
                    <td><input name="${idNominal}" type="text" /></td>
                    <td><input name="${idVerification}" type="text" /></td>
                    <td>
                      <select name="unit_${i}_${point}">
                        <option value="${selectedUnit}">${selectedUnit}</option>
                      </select>
                    </td>
                    <td><input name="observation_${i}_${conductor}" type="text" /></td>
                    <td>
                        <label class="camera-label">
                            📷 <span class="attach-text"></span>
                            <input type="file" accept="image/*" name="image_${i}_${conductor}" style="display:none;" />
                        </label>
                    </td>
                `;
                table.appendChild(row);

                const label = row.querySelector("label");
                const inputFile = label.querySelector("input[type='file']");
                const textAttach = label.querySelector(".attach-text");

                inputFile.addEventListener("change", () => {
                    textAttach.textContent = inputFile.files.length ? "📎 File attached" : "";
                });
            });

            resultContainer.appendChild(table);
        }
    }

    cableSetInput.addEventListener("input", generateFields);
    generateFields();

    document.getElementById("test-form").addEventListener("submit", async function (e) {
        const type = document.getElementById("test-type")?.value;
        if (type !== "torque") return;

        e.preventDefault();

        const cableSets = parseInt(cableSetInput.value);
        if (!cableSets) {
            alert("Enter cable set quantity.");
            return;
        }

        const data = [];
        const images = [];

        const project_id = document.getElementById("project_id").value;
        const location_1 = document.getElementById("location_1").value;
        const number_location_1 = document.getElementById("number_location_1").value;
        const location_2 = document.getElementById("location_2")?.value || "";
        const number_location_2 = document.getElementById("number_location_2")?.value || "";
        const equipment_type = document.getElementById("equipment_type").value;
        const number_equipment_type = document.getElementById("number_equipment_type").value;
        const sub_equipment = document.getElementById("sub_equipment")?.value || "";
        const number_sub_equipment = document.getElementById("number_sub_equipment")?.value || "";
        const power_type = document.getElementById("power_type")?.value;
        const terminal = document.getElementById("terminal")?.value || "";
        

        for (let i = 1; i <= cableSets; i++) {
            for (const conductor of conductors) {
                const nominal = document.querySelector(`[name="nominal_${i}_${conductor}"]`)?.value || "";
                const verification = document.querySelector(`[name="verification_${i}_${conductor}"]`)?.value || "";
                const observation = document.querySelector(`[name="observation_${i}_${conductor}"]`)?.value || "";
                const imageInput = document.querySelector(`[name="image_${i}_${conductor}"]`);
                const image = imageInput?.files[0];

                data.push({
                    cable_set: i,
                    test_point: conductor,
                    nominal_value: nominal,
                    verification_value: verification,
                    unit: selectedUnit,
                    observation: observation
                });

                images.push(image || new File([], ""));
            }
        }

        const formData = new FormData();
        formData.append("project_id", project_id);
        formData.append("location_1", location_1);
        formData.append("number_location_1", number_location_1);
        formData.append("location_2", location_2);
        formData.append("number_location_2", number_location_2);
        formData.append("equipment_type", equipment_type);
        formData.append("number_equipment_type", number_equipment_type);
        formData.append("sub_equipment", sub_equipment);
        formData.append("number_sub_equipment", number_sub_equipment);
        formData.append("test_type", "torque");
        formData.append("cable_sets", cableSets);
        formData.append("power_type", power_type);
        formData.append("terminal", terminal);
        formData.append("data", JSON.stringify(data));
        images.forEach((img) => formData.append("images", img));

        const response = await fetch("/form/torque/save", {
            method: "POST",
            body: formData
        });

        const res = await response.json().catch(() => null);
        if (response.ok && res?.message) {
            alert(res.message);
        } else {
            alert(res?.detail || "Error saving form.");
        }
    });
}

window.initFormTorque = initFormTorque;

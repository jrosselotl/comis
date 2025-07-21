function initFormContinuity(powerType) {
    const cableSetInput = document.getElementById("cable_sets");
    const selectedUnit = document.getElementById("unit")?.value || "";
    const resultContainer = document.getElementById("result-container");
    const resultBlock = document.getElementById("result-block");

    const point = powerType === "single_phase"
        ? ["L", "N", "PE"]
        : ["L1", "L2", "L3", "N", "PE"];

    function generateCombination(list) {
        const combo = [];
        for (let i = 0; i < list.length; i++) {
            for (let j = i + 1; j < list.length; j++) {
                combo.push(`${list[i]}-${list[j]}`);
            }
        }
        return combo;
    }

    const combination = generateCombination(point);

    function generateFields() {
        const quantity = parseInt(cableSetInput.value) || 0;
        resultContainer.innerHTML = "";
        resultBlock.style.display = quantity > 0 ? "block" : "none";

        // ✅ Load global unit select
        if (window.UNIT_BY_TEST && window.UNIT_BY_TEST["continuity"]) {
            const unitSelect = document.getElementById("unit");
            const labelUnit = document.getElementById("label-unit");

            if (unitSelect && labelUnit) {
                unitSelect.innerHTML = '<option value="">Select unit...</option>';
                window.UNIT_BY_TEST["continuity"].forEach((u) => {
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
                <caption>Continuity - Cable Set ${i}</caption>
                <tr>
                    <th>Point</th>
                    <th>Result / N/A</th>
                    <th>Unit</th>
                    <th>Observation</th>
                    <th>Image</th>
                </tr>`;

            combination.forEach((point) => {
                const row = document.createElement("tr");
                const idResult = `result_${i}_${point}`;
                const idNA = `na_${i}_${point}`;

                row.innerHTML = `
                    <td>${point}</td>
                    <td>
                        <div class="result-combined">
                            <button type="button" class="na-btn" id="${idNA}">N/A</button>
                            <input type="text" name="${idResult}" id="${idResult}" />
                        </div>
                    </td>
                    <td>
                    <input type="text" name="unit_${i}_${point}" value="${selectedUnit}" readonly />
                    </td>
                    <td><input name="observation_${i}_${point}" type="text" /></td>
                    <td>
                        <label class="camera-label">
                            📷 <span class="attach-text"></span>
                            <input type="file" accept="image/*" name="image_${i}_${point}" style="display:none;" />
                        </label>
                    </td>
                `;
                table.appendChild(row);

                const inputResult = row.querySelector(`#${idResult}`);
                const buttonNA = row.querySelector(`#${idNA}`);

                buttonNA.addEventListener("click", () => {
                    inputResult.disabled = !inputResult.disabled;
                    inputResult.value = inputResult.disabled ? "N/A" : "";
                    buttonNA.classList.toggle("active");
                });

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

    document.getElementById("form-test").addEventListener("submit", async function (e) {
        const type = document.getElementById("test-type")?.value;
        if (type !== "continuity") return;

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
            for (const point of combination) {
                const result = document.querySelector(`[name="result_${i}_${point}"]`)?.value || "";
                const observation = document.querySelector(`[name="observation_${i}_${point}"]`)?.value || "";
                const imageInput = document.querySelector(`[name="image_${i}_${point}"]`);
                const image = imageInput?.files[0];

                data.push({
                    cable_set: i,
                    test_point: point,
                    result_value: result,
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
        formData.append("test_type", "continuity");
        formData.append("cable_sets", cableSets);
        formData.append("power_type", power_type);
        formData.append("terminal", terminal);
        formData.append("data", JSON.stringify(data));
        images.forEach((img) => formData.append("images", img));

        const response = await fetch("/form/continuity/save", {
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

window.initFormContinuity = initFormContinuity;

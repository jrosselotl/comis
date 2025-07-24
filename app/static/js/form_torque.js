function initFormTorque(powerType) {
    const cableSetInput = document.getElementById("cable_set");
    const resultContainer = document.getElementById("result-container");
    const resultBlock = document.getElementById("result-block");

    const conductors = powerType === "single_phase"
        ? ["L", "N", "PE"]
        : ["L1", "L2", "L3", "N", "PE"];

    function generateFields() {
        const quantity = parseInt(cableSetInput.value) || 0;
        resultContainer.innerHTML = "";
        resultBlock.style.display = quantity > 0 ? "block" : "none";

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

        const selectedUnit = document.getElementById("unit")?.value || "";
        for (let i = 1; i <= quantity; i++) {
            const table = document.createElement("table");
            table.classList.add("test-table");

            table.innerHTML = `
                <caption>Torque - Cable Set ${i}</caption>
                <tr>
                    <th>Point</th>
                    <th>Nominal Value</th>
                    <th>Verification Value</th>
                    <th>Unit</th>
                    <th>Observation</th>
                    <th>Image</th>
                </tr>`;

            conductors.forEach((point) => {
                const row = document.createElement("tr");
                const idNominal = `nominal_${i}_${point}`;
                const idVerification = `verification_${i}_${point}`;

                row.innerHTML = `
                    <td>${point}</td>
                    <td><input name="${idNominal}" type="text" /></td>
                    <td><input name="${idVerification}" type="text" /></td>
                    <td><input type="text" value="${selectedUnit}" readonly name="unit_${i}_${point}" /></td>
                    <td><input name="observation_${i}_${point}" type="text" /></td>
                    <td>
                        <label class="camera-label">
                            📷 <span class="attach-text"></span>
                            <input type="file" accept="image/*" name="image_${i}_${point}" style="display:none;" />
                        </label>
                    </td>
                `;
                table.appendChild(row);

                const label = row.querySelector("label");
                const inputFile = label.querySelector("input[type='file']");
                const attachText = label.querySelector(".attach-text");

                inputFile.addEventListener("change", () => {
                    attachText.textContent = inputFile.files.length ? "📎 File attached" : "";
                });
            });

            resultContainer.appendChild(table);
        }
    }

    cableSetInput.addEventListener("input", generateFields);
    generateFields();

    document.getElementById("form-test").addEventListener("submit", async function (e) {
        const type = document.getElementById("test-type")?.value;
        if (type !== "torque") return;

        e.preventDefault();

        const cableSets = parseInt(cableSetInput.value);
        if (!cableSets) {
            alert("Enter cable set quantity.");
            return;
        }

        const results = [];
        const formData = new FormData();

        const project_id = document.getElementById("project_id").value;
        const equipment_id = document.getElementById("equipment_id")?.value || 0;
        const user_id = window.CURRENT_USER_ID || 1;
        const test_id = document.getElementById("test-type").value;

        for (let i = 1; i <= cableSets; i++) {
            for (const point of conductors) {
                const nominal = document.querySelector(`[name="nominal_${i}_${point}"]`)?.value || "";
                const verification = document.querySelector(`[name="verification_${i}_${point}"]`)?.value || "";
                const observation = document.querySelector(`[name="observation_${i}_${point}"]`)?.value || "";
                const imageInput = document.querySelector(`[name="image_${i}_${point}"]`);
                const image = imageInput?.files[0];

                results.push({
                    cable_set: i,
                    test_point: point,
                    nominal_value: nominal ? parseFloat(nominal) : null,
                    verification_value: verification ? parseFloat(verification) : null,
                    unit: document.getElementById("unit")?.value || "",
                    observation: observation,
                    image_field: `image_${i}_${point}`
                });

                if (image) {
                    formData.append(`image_${i}_${point}`, image);
                }
            }
        }

        formData.append("project_id", project_id);
        formData.append("equipment_id", equipment_id);
        formData.append("user_id", user_id);
        formData.append("test_id", test_id);
        formData.append("status", "completed");
        formData.append("results", JSON.stringify(results));

        try {
            const response = await fetch("/test_performed/create", {
                method: "POST",
                body: formData
            });

            const res = await response.json();
            if (response.ok) {
                alert(res.message || "✅ Torque test saved successfully");
            } else {
                alert(res.detail || "❌ Error saving torque test");
            }
        } catch (err) {
            console.error(err);
            alert("❌ Error connecting to server");
        }
    });
}

window.initFormTorque = initFormTorque;

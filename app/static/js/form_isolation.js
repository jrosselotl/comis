function initFormIsolation(powerType) {
    const cableSetInput = document.getElementById("cable_set");
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

        const selectedUnit = document.getElementById("unit")?.value || "";
        for (let i = 1; i <= quantity; i++) {
            const table = document.createElement("table");
            table.classList.add("test-table");

            table.innerHTML = `
                <caption>Isolation - Cable Set ${i}</caption>
                <tr>
                    <th>Point</th>
                    <th>Result / N/A</th>
                    <th>Unit</th>
                    <th>Applied Time (s)</th>
                    <th>Observation</th>
                    <th>Image</th>
                </tr>`;

            combination.forEach((point) => {
                const row = document.createElement("tr");
                const idResult = `result_${i}_${point}`;
                const idNA = `na_${i}_${point}`;
                const idTime = `time_${i}_${point}`;

                row.innerHTML = `
                    <td>${point}</td>
                    <td>
                        <div class="result-combined">
                            <button type="button" class="na-btn" id="${idNA}">N/A</button>
                            <input type="text" name="${idResult}" id="${idResult}" />
                        </div>
                    </td>
                    <td><input type="text" value="${selectedUnit}" readonly name="unit_${i}_${point}" /></td>
                    <td><input name="${idTime}" type="number" /></td>
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
        if (type !== "isolation") return;

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
            for (const point of combination) {
                const result = document.querySelector(`[name="result_${i}_${point}"]`)?.value || "";
                const time_applied = document.querySelector(`[name="time_${i}_${point}"]`)?.value || "";
                const observation = document.querySelector(`[name="observation_${i}_${point}"]`)?.value || "";
                const imageInput = document.querySelector(`[name="image_${i}_${point}"]`);
                const image = imageInput?.files[0];

                results.push({
                    cable_set: i,
                    test_point: point,
                    result_value: result === "N/A" ? null : parseFloat(result) || null,
                    time_applied: time_applied ? parseFloat(time_applied) : null,
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
                alert(res.message || "✅ Isolation test saved successfully");
            } else {
                alert(res.detail || "❌ Error saving isolation test");
            }
        } catch (err) {
            console.error(err);
            alert("❌ Error connecting to server");
        }
    });
}

window.initFormIsolation = initFormIsolation;

function initFormTorque(powerType) {
    const cableSetInput = document.getElementById("cable_sets");
    const resultContainer = document.getElementById("result-container");
    const resultBlock = document.getElementById("result-block");

    // ✅ Torque uses individual conductors, no combinations
    const conductors = powerType === "single_phase"
        ? ["L", "N", "PE"]
        : ["L1", "L2", "L3", "N", "PE"];

    function generateFields() {
        const quantity = parseInt(cableSetInput.value) || 0;
        resultContainer.innerHTML = "";
        resultBlock.style.display = quantity > 0 ? "block" : "none";

        for (let i = 1; i <= quantity; i++) {
            const table = document.createElement("table");
            table.classList.add("test-table");

            table.innerHTML = `
                <caption>Torque - Cable Set ${i}</caption>
                <tr>
                    <th>Conductor</th>
                    <th>Nominal Value</th>
                    <th>Check Value</th>
                    <th>Unit</th>
                    <th>Observation</th>
                    <th>Image</th>
                </tr>`;

            conductors.forEach((conductor) => {
                const row = document.createElement("tr");
                const idNominal = `nominal_${i}_${conductor}`;
                const idCheck = `check_${i}_${conductor}`;

                row.innerHTML = `
                    <td>${conductor}</td>
                    <td><input name="${idNominal}" type="text" /></td>
                    <td><input name="${idCheck}" type="text" /></td>
                    <td><input name="unit_${i}_${conductor}" type="text" /></td>
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
        const number_location_

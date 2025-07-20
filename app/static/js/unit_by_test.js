// static/js/unidades_por_test.js

(function () {
    const UNIT_BY_TEST = {
        continuity: ["Ω", "mΩ", "kΩ"],
        isolation: ["MΩ", "GΩ", "kΩ"],
        contact_resistance: ["µΩ", "mΩ", "Ω"],
        torque: ["Nm", "Nmm", "kNm"],
        voltage: ["V", "mV", "kV"],
        current: ["A", "mA", "kA", "µA"],
        time: ["ms", "s", "min", "h"]
        // Future: pressure: ["bar", "psi", "kPa"]
    };

    // Prevent redefinition if already defined globally
    if (!window.UNIT_BY_TEST) {
        window.UNIT_BY_TEST = UNIT_BY_TEST;
    } else {
        console.warn("UNIT_BY_TEST was already defined in the global context.");
    }
})();

/**
 * Dynamically loads unit into the <select> based on the test type
 * @param {string} testType - The test type (e.g., "continuity", "torque")
 */
function loadUnitByTest(testType) {
    const unitSelect = document.getElementById("unit");
    const labelUnit = document.getElementById("label-unit");

    if (!unitSelect || !labelUnit) {
        console.warn("Unit select or label not found in the DOM.");
        return;
    }

    unitSelect.innerHTML = '<option value="">Select unit...</option>';

    const unit = window.UNIT_BY_TEST[testType] || [];
    if (unit.length > 0) {
        unit.forEach(unit => {
            const option = document.createElement("option");
            option.value = unit;
            option.textContent = unit;
            unitSelect.appendChild(option);
        });
        labelUnit.style.display = "block";
    } else {
        labelUnit.style.display = "none";
    }
}

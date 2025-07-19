// static/js/unidades_por_test.js

(function () {
    const UNITS_BY_TEST = {
        continuity: ["Ω", "mΩ", "kΩ", "MΩ"],
        isolation: ["MΩ", "GΩ", "kΩ"],
        contact_resistance: ["µΩ", "mΩ", "Ω"],
        torque: ["Nm", "Nmm", "kNm"],
        voltage: ["V", "mV", "kV"],
        current: ["A", "mA", "kA", "µA"],
        time: ["ms", "s", "min", "h"]
        // Future: pressure: ["bar", "psi", "kPa"]
    };

    // Prevent redefinition if already defined globally
    if (!window.UNITS_BY_TEST) {
        window.UNITS_BY_TEST = UNITS_BY_TEST;
    } else {
        console.warn("UNITS_BY_TEST was already defined in the global context.");
    }
})();

/**
 * Dynamically loads units into the <select> based on the test type
 * @param {string} testType - The test type (e.g., "continuity", "torque")
 */
function loadUnitsByTest(testType) {
    const unitSelect = document.getElementById("unit");
    const labelUnit = document.getElementById("label-unit");

    if (!unitSelect || !labelUnit) {
        console.warn("Unit select or label not found in the DOM.");
        return;
    }

    unitSelect.innerHTML = '<option value="">Select unit...</option>';

    const units = window.UNITS_BY_TEST[testType] || [];
    if (units.length > 0) {
        units.forEach(unit => {
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

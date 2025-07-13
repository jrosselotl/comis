// static/js/unidades_por_test.js

(function () {
    const UNIDADES_POR_TEST = {
        continuidad: ["Ω", "mΩ", "kΩ", "MΩ"],
        megado: ["MΩ", "GΩ", "kΩ"],
        contact_resistance: ["µΩ", "mΩ", "Ω"],
        torque: ["Nm", "Nmm", "kNm"],
        voltaje: ["V", "mV", "kV"],
        corriente: ["A", "mA", "kA", "µA"],
        tiempo: ["ms", "s", "min", "h"]
        // Futuro: presion: ["bar", "psi", "kPa"]
    };

    // Validación simple por si ya fue definida
    if (!window.UNIDADES_POR_TEST) {
        window.UNIDADES_POR_TEST = UNIDADES_POR_TEST;
    } else {
        console.warn("UNIDADES_POR_TEST ya estaba definida en el contexto global.");
    }
})();

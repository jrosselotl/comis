document.addEventListener("DOMContentLoaded", async function () {
    // Cargar lista de proyectos
    const select = document.getElementById("proyecto-id");
    try {
        const res = await fetch("/proyectos/");  // ← CAMBIO AQUÍ
        const data = await res.json();
        select.innerHTML = "";
        data.forEach(p => {
            const opt = document.createElement("option");
            opt.value = p.id;
            opt.textContent = p.nombre;
            select.appendChild(opt);
        });
    } catch {
        select.innerHTML = `<option value="">Error cargando proyectos</option>`;
    }

    // Cargar JS dinámico según tipo de prueba
    const tipoPruebaSelect = document.getElementById("tipo-prueba");
    let currentScript;

   async function loadScript() {
    if (currentScript) currentScript.remove();

    const tipo = tipoPruebaSelect.value;

    // No hacer nada si no se seleccionó tipo de prueba
    if (!tipo) return;

    currentScript = document.createElement("script");
    currentScript.src = tipo === "megado" 
        ? "/static/js/formulario_megado.js" 
        : "/static/js/formulario_continuidad.js";
    document.body.appendChild(currentScript);
}

    tipoPruebaSelect.addEventListener("change", loadScript);
    if (tipoPruebaSelect.value) {
    await loadScript();
}
});

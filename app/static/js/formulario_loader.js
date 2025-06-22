document.addEventListener("DOMContentLoaded", async function () {
    // Cargar lista de proyectos
    const select = document.getElementById("proyecto-id");
    try {
        const res = await fetch("/proyectos/");  
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

    
const scriptMap = {
    continuidad: "/static/js/formulario_continuidad.js",
    megado: "/static/js/formulario_megado.js",
    ductor: "/static/js/formulario_ductor.js",
    // ... puedes agregar más aquí
};
async function loadScript() {
    if (currentScript) currentScript.remove();

    const tipo = tipoPruebaSelect.value;

    if (!scriptMap[tipo]) return;  // Si no hay script para el tipo, no hace nada

    currentScript = document.createElement("script");
    currentScript.src = scriptMap[tipo];
    document.body.appendChild(currentScript);
}


    tipoPruebaSelect.addEventListener("change", loadScript);
    if (tipoPruebaSelect.value) {
    await loadScript();
}
});

const personas = [];

document
  .getElementById("form-persona")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    const persona = {
      nombre: document.getElementById("nombre").value.trim(),
      direccion: document.getElementById("direccion").value.trim(),
      dni: document.getElementById("dni").value.trim(),
      campos: [
        document.getElementById("primarios").checked ? "S" : "N",
        document.getElementById("secundarios").checked ? "S" : "N",
        document.getElementById("universitarios").checked ? "S" : "N",
        document.getElementById("vivienda").checked ? "S" : "N",
        document.getElementById("obra").checked ? "S" : "N",
        document.getElementById("trabaja").checked ? "S" : "N",
        document.getElementById("otro1").checked ? "S" : "N",
        document.getElementById("otro2").checked ? "S" : "N",
      ],
    };

    personas.push(persona);
    mostrarResultados();
    this.reset();
  });

function mostrarResultados() {
  // Simulación longitud fija
  const fijos = personas
    .map((p) => {
      return (
        p.nombre.padEnd(30, " ") +
        p.direccion.padEnd(50, " ") +
        p.dni.padEnd(10, " ") +
        p.campos.join("")
      );
    })
    .join("\n");

  // Simulación longitud variable (JSON)
  const variable = JSON.stringify(personas);

  // Calcular tamaños
  const tamFijos = new Blob([fijos]).size;
  const tamVariable = new Blob([variable]).size;

  document.getElementById("resultados").textContent =
    "Archivo fijos.dat:\n" +
    fijos +
    "\n\nArchivo variable.dat:\n" +
    variable +
    `\n\nTamaño fijos.dat: ${tamFijos} bytes` +
    `\nTamaño variable.dat: ${tamVariable} bytes`;
}

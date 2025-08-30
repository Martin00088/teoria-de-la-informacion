// Función para validar CUIT/CUIL
function validarCUIT(cuit) {
  // Quitar guiones y espacios
  cuit = cuit.replace(/[-\s]/g, "");

  // Debe tener 11 dígitos
  if (!/^\d{11}$/.test(cuit)) {
    return false;
  }

  // Coeficientes para calcular el dígito verificador
  const coeficientes = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2];

  let suma = 0;
  for (let i = 0; i < 10; i++) {
    suma += parseInt(cuit[i]) * coeficientes[i];
  }

  let verificador = 11 - (suma % 11);
  if (verificador === 11) verificador = 0;
  if (verificador === 10) verificador = 9;

  // Compara el dígito verificador calculado con el ingresado
  return verificador === parseInt(cuit[10]);
}

// Pedir al usuario que ingrese el CUIT/CUIL
const readline = require("readline").createInterface({
  input: process.stdin,
  output: process.stdout,
});

readline.question("Ingrese un CUIT/CUIL: ", (cuit) => {
  if (validarCUIT(cuit)) {
    console.log("CUIT/CUIL válido.");
  } else {
    console.log("CUIT/CUIL inválido.");
  }
  readline.close();
});

// Elimina guiones o espacios que pueda haber en el ingreso.
// Verifica que tenga exactamente 11 dígitos.
// Calcula el dígito verificador usando los coeficientes específicos.
// Compara el dígito calculado con el último dígito del CUIT/CUIL ingresado.
// Devuelve si es válido o no.

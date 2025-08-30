function simpleSimilarity(str1, str2) {
  // Convertimos todo a minúsculas para evitar diferencias por mayúsculas
  str1 = str1.toLowerCase();
  str2 = str2.toLowerCase();

  let matches = 0;

  // Contamos cuántos caracteres de str1 están en str2
  for (let char of str1) {
    if (str2.includes(char)) {
      matches++;
      // Quitamos el carácter de str2 para no contarlo dos veces
      str2 = str2.replace(char, "");
    }
  }

  // Calculamos el porcentaje respecto a la longitud de str1
  return ((matches / str1.length) * 100).toFixed(2);
}

// Ejemplos
console.log(simpleSimilarity("Juan Perez", "Jaun Perez") + "%"); // Similaridad alta
console.log(simpleSimilarity("Horacio López", "Oracio López") + "%"); // Similaridad alta
console.log(simpleSimilarity("Carlos", "Maria") + "%"); // Similaridad baja

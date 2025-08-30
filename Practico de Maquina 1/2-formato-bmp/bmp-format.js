const fs = require("fs");
const path = require("path");
const readline = require("readline");

function readBmpHeader(buffer) {
  return {
    Signature: buffer.toString("ascii", 0, 2),
    FileSize: buffer.readUInt32LE(2),
    Reserved: buffer.readUInt32LE(6),
    DataOffset: buffer.readUInt32LE(10),
    Size: buffer.readUInt32LE(14),
    Width: buffer.readUInt32LE(18),
    Height: buffer.readUInt32LE(22),
    Planes: buffer.readUInt16LE(26),
    BitCount: buffer.readUInt16LE(28),
    Compression: buffer.readUInt32LE(30),
    ImageSize: buffer.readUInt32LE(34),
    XPixelsPerM: buffer.readUInt32LE(38),
    YPixelsPerM: buffer.readUInt32LE(42),
    ColorsUsed: buffer.readUInt32LE(46),
    ColorsImportant: buffer.readUInt32LE(50),
  };
}

function validateBmp(header) {
  return header.Signature === "BM";
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

rl.question("Ingrese el nombre del archivo .bmp: ", (filename) => {
  const filePath = path.resolve(filename);

  if (!fs.existsSync(filePath)) {
    console.error("❌ El archivo no existe.");
    rl.close();
    return;
  }

  const buffer = fs.readFileSync(filePath);

  if (buffer.length < 54) {
    console.error("❌ El archivo es demasiado pequeño para ser un BMP válido.");
    rl.close();
    return;
  }

  const header = readBmpHeader(buffer);

  if (!validateBmp(header)) {
    console.error("❌ El archivo no tiene el formato BMP esperado.");
  } else {
    console.log("✅ Cabecera BMP:");
    console.table(header);
  }

  rl.close();
});

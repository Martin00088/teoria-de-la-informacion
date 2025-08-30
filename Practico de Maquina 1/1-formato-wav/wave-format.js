const fs = require("fs");
const path = require("path");
const readline = require("readline");

function readWavHeader(buffer) {
  return {
    ChunkID: buffer.toString("ascii", 0, 4),
    ChunkSize: buffer.readUInt32LE(4),
    Format: buffer.toString("ascii", 8, 12),
    Subchunk1ID: buffer.toString("ascii", 12, 16),
    Subchunk1Size: buffer.readUInt32LE(16),
    AudioFormat: buffer.readUInt16LE(20),
    NumChannels: buffer.readUInt16LE(22),
    SampleRate: buffer.readUInt32LE(24),
    ByteRate: buffer.readUInt32LE(28),
    BlockAlign: buffer.readUInt16LE(32),
    BitsPerSample: buffer.readUInt16LE(34),
    Subchunk2ID: buffer.toString("ascii", 36, 40),
    Subchunk2Size: buffer.readUInt32LE(40),
  };
}

function validateWav(header) {
  return (
    header.ChunkID === "RIFF" &&
    header.Format === "WAVE" &&
    header.Subchunk1ID === "fmt " &&
    header.Subchunk2ID === "data"
  );
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

rl.question("Ingrese el nombre del archivo .wav: ", (filename) => {
  const filePath = path.resolve(filename);

  if (!fs.existsSync(filePath)) {
    console.error("❌ El archivo no existe.");
    rl.close();
    return;
  }

  const buffer = fs.readFileSync(filePath);

  if (buffer.length < 44) {
    console.error("❌ El archivo es demasiado pequeño para ser un WAV válido.");
    rl.close();
    return;
  }

  const header = readWavHeader(buffer);

  if (!validateWav(header)) {
    console.error("❌ El archivo no tiene el formato WAV esperado.");
  } else {
    console.log("✅ Cabecera WAV:");
    console.table(header);
  }

  rl.close();
});

const sum = (arr: number[]): number => arr.reduce((a, b) => a + b, 0);

export class Shannon {
  constructor(probabilities: Record<string, number>, base: number = 2) {
    if (Math.abs(sum(Object.values(probabilities)) - 1) > 0.01) {
      throw new Error("Probabilities must sum 1");
    }
    this.probabilities = probabilities;
    this.base = base;

    this._makeCodes();
    const codesList = Object.values(this.codes);

    for (const symbol of this.symbols) {
      if (!this.codes[symbol]) {
        throw new Error("All symbols must have a code");
      }

      const code = this.codes[symbol];
      if (codesList.some((c) => code.startsWith(c) && code !== c)) {
        throw new Error("Codes must be prefix-free");
      }
    }
  }
  public readonly probabilities: Record<string, number>;
  public readonly codes: Record<string, string> = {};
  public readonly base: number;

  get symbols(): string[] {
    return Object.keys(this.probabilities);
  }

  public encodeOne(str: string): [string, string] {
    const symbol = this.symbols.find((symbol) => str.startsWith(symbol));

    if (!symbol) throw new Error("Invalid symbol");

    return [symbol, this.codes[symbol]!];
  }

  public encode(str: string): string {
    let encoded = "";
    while (str.length) {
      const [symbol, code] = this.encodeOne(str);

      encoded += code;
      str = str.slice(symbol.length);
    }

    return encoded;
  }

  public decodeOne(str: string): [string, string] {
    const symbol = this.symbols.find((symbol) =>
      str.startsWith(this.codes[symbol]!)
    );

    if (!symbol) throw new Error("Invalid symbol");

    return [symbol, this.codes[symbol]!];
  }

  public decode(str: string): string {
    let decoded = "";
    while (str.length) {
      const [symbol, code] = this.decodeOne(str);

      decoded += symbol;
      str = str.slice(code.length);
    }

    return decoded;
  }

  private _makeCode(length: number, symbol: string): string {
    let num = 0;
    console.log("Making code of length:", length);

    while (num < this.base ** length) {
      const code = num.toString(this.base).padStart(length, "0");
      //Detectar Conflictos con los codigos existentes
      const conflict = Object.values(this.codes).some(
        (c) => code.startsWith(c) || c.startsWith(code)
      );
      if (!conflict) {
        console.log(`✅ Código elegido para "${symbol}": ${code}`);
        return code;
      } else {
        console.log(
          `⚠️ Conflicto: "${code}" entra en conflicto con "${conflict}"`
        );
      }
      num++;
    }
    throw new Error("No code found");
  }

  protected _makeCodes(): void {
    console.log("\n🧮 Iniciando generación de códigos Shannon...");
    for (const symbol of this.symbols) {
      const length = Math.ceil(
        -Math.log2(this.probabilities[symbol]!.valueOf())
      );
      console.log(`\n🔹 Símbolo: "${symbol}"`);
      console.log(`   Probabilidad: ${this.probabilities[symbol]}`);
      console.log(`   Longitud teórica: ${length}`);
      // const length = this.probabilities[symbol]!.log2().neg().ceil().valueOf();;

      this.codes[symbol] = this._makeCode(length, symbol);
    }
  }
}

const subdivideString = (str: string, order: number): string[] => {
  const substrings: string[] = [];
  for (let i = 0; i < str.length - order + 1; i++) {
    substrings.push(str.slice(i, i + order));
  }

  return substrings;
};

class Markov {
  constructor(str: string, order = 1) {
    this.symbols = Array.from(new Set(str.split(""))).sort();
    this.order = order;

    const l = Math.ceil(Math.log2(this.symbols.length));
    this.pseudoASCIILength = l;
    this.pseudoASCII = {};
    for (let i = 0; i < this.symbols.length; i++) {
      this.pseudoASCII[this.symbols[i]] = i.toString(2).padStart(l, "0");
    }

    this._makeCodes(str);
  }
  public readonly symbols: string[];
  public readonly order: number;
  public readonly pseudoASCIILength: number;
  public readonly pseudoASCII: Record<string, string>;
  public readonly codifications: {
    [key: string]: Shannon;
  } = {};

  private _makeCodes(str: string): void {
    const divisions = subdivideString(str, this.order + 1);
    const keys = [...new Set(divisions.map((str) => str.slice(0, -1)))];

    for (const key of keys) {
      const uses = divisions.filter((str) => str.startsWith(key));
      const probabilities: Record<string, number> = {};

      for (const use of uses) {
        const symbol = use.slice(-1);
        probabilities[symbol] = (probabilities[symbol] || 0) + 1;
      }

      for (const symbol in probabilities) {
        probabilities[symbol] = probabilities[symbol] / uses.length;
      }
      console.log(`\n📈 Contexto "${key}" -> Probabilidades:`, probabilities);
      this.codifications[key] = new Shannon(probabilities);
      console.log(
        `📊 Códigos para contexto "${key}":`,
        this.codifications[key].codes
      );
    }
    // 🔍 Nuevo bloque: detectar conflictos entre contextos
    // console.log("\n🚨 Verificando conflictos entre contextos...");
    // const contexts = Object.entries(this.codifications);
    // for (let i = 0; i < contexts.length; i++) {
    //   const [ctxA, shannonA] = contexts[i];
    //   for (let j = i + 1; j < contexts.length; j++) {
    //     const [ctxB, shannonB] = contexts[j];

    //     for (const [symA, codeA] of Object.entries(shannonA.codes)) {
    //       for (const [symB, codeB] of Object.entries(shannonB.codes)) {
    //         if (codeA.startsWith(codeB) || codeB.startsWith(codeA)) {
    //           console.log(
    //             `⚠️ Conflicto entre contextos "${ctxA}" y "${ctxB}": Código "${codeA}" para símbolo "${symA}" y código "${codeB}" para símbolo "${symB}"`
    //           );
    //         }
    //       }
    //     }
    //   }
    // }
    // console.log("✅ Verificación de conflictos entre contextos completada.\n");
  }

  public encodeASCII(str: string): string {
    return this.symbols
      .findIndex((x) => x === str[0])
      .toString(2)
      .padStart(this.pseudoASCIILength, "0");
  }

  public encode(str: string): string {
    let encoded = "";
    for (let i = 0; i < this.order; i++) {
      encoded += this.encodeASCII(str[i]);
    }

    let prev = str.slice(0, this.order);
    for (let i = this.order; i < str.length; i++) {
      encoded += this.codifications[prev]!.encode(str[i]!);
      prev = prev.slice(1) + str[i];
    }

    return encoded;
  }

  public decodeASCII(str: string): [string, string] {
    const code = str.slice(0, this.pseudoASCIILength);
    const symbol = this.symbols[parseInt(code, 2)];

    return [symbol, code];
  }

  public decode(str: string): string {
    let decoded = "";

    while (str.length) {
      const [symbol, code] =
        decoded.length < this.order
          ? this.decodeASCII(str)
          : this.codifications[decoded.slice(-this.order)]!.decodeOne(str);

      decoded += symbol;
      str = str.slice(code.length);
    }

    return decoded;
  }
}

// const str =
//   "https://www.geeknetic.es/Noticia/17666/Winrar-vs-7-Zip-vs-Winzip-Cual-es-el-mejor-descompresor-para-Windows.html";
const str = "YOHAGOYOGAHOYY";
// const str = "";
const grado = 1;

const markovShannon = new Markov(str, grado);
const encodedShannon = markovShannon.encode(str);
const decodedShannon = markovShannon.decode(encodedShannon);

// console.log("Markov:", markovShannon.codifications);
// console.log(
//   "Codificacion 1 probabilidad:",
//   markovShannon.codifications[0].probabilities
// );
// console.log("Codificacion 1 codes:", markovShannon.codifications[0].codes);
console.log("Codigo Comprimido Shannon-Markov:", encodedShannon);
// console.log("Codigo Descomprimido Shannon-Markov:", encodedShannon);

console.log(
  "Codigo sin comprimir===Codigo descomprimido ",
  str === decodedShannon
);

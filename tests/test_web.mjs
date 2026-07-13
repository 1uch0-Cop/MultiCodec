import test from "node:test";
import assert from "node:assert/strict";

import {
    INVALID_BASE64,
    INVALID_BASE64_TEXT,
    INVALID_BINARY,
    INVALID_BINARY_TEXT,
    INVALID_HEX,
    INVALID_HEX_TEXT,
    INVALID_URL,
    binaryToDecimal,
    binaryToHex,
    binaryToText,
    convertValue,
    decodeBase64,
    decodeHex,
    decodeUrl,
    encodeBase64,
    encodeHex,
    encodeUrl,
    formatSmartResults,
    rot13,
    smartDecode,
    textToBinary,
} from "../web/multicodec.js";


test("Base64 conserva texto UTF-8", () => {
    const original = "Zorro ñ 🦊";

    assert.equal(
        decodeBase64(encodeBase64(original)),
        original,
    );
});


test("Base64 rechaza una entrada inválida", () => {
    assert.equal(
        decodeBase64("%%%"),
        INVALID_BASE64,
    );
});


test("Base64 detecta contenido no UTF-8", () => {
    assert.equal(
        decodeBase64("/w=="),
        INVALID_BASE64_TEXT,
    );
});


test("Hexadecimal conserva texto UTF-8", () => {
    const original = "Atacama 🦊";

    assert.equal(
        decodeHex(encodeHex(original)),
        original,
    );
});


test("Hexadecimal acepta espacios", () => {
    assert.equal(
        decodeHex("68 6f 6c 61"),
        "hola",
    );
});


test("Hexadecimal rechaza entrada inválida", () => {
    assert.equal(
        decodeHex("68-6f"),
        INVALID_HEX,
    );
});


test("Hexadecimal detecta contenido no UTF-8", () => {
    assert.equal(
        decodeHex("ff"),
        INVALID_HEX_TEXT,
    );
});


test("ROT13 es reversible", () => {
    const original = "Ataque al amanecer";

    assert.equal(
        rot13(rot13(original)),
        original,
    );
});


test("URL conserva texto UTF-8", () => {
    const original = "hola / mundo ñ 🦊";

    assert.equal(
        decodeUrl(encodeUrl(original)),
        original,
    );
});


test("URL rechaza porcentajes inválidos", () => {
    assert.equal(
        decodeUrl("%GG"),
        INVALID_URL,
    );
});


test("Binario usa bytes UTF-8", () => {
    assert.equal(
        textToBinary("ñ"),
        "11000011 10110001",
    );
});


test("Binario conserva texto UTF-8", () => {
    const original = "Atacama 🦊";

    assert.equal(
        binaryToText(textToBinary(original)),
        original,
    );
});


test("Binario rechaza longitud incorrecta", () => {
    assert.equal(
        binaryToText("0101"),
        INVALID_BINARY,
    );
});


test("Binario detecta contenido no UTF-8", () => {
    assert.equal(
        binaryToText("11111111"),
        INVALID_BINARY_TEXT,
    );
});


test("Binario convierte a decimal con BigInt", () => {
    assert.equal(
        binaryToDecimal(
            "01101000011011110110110001100001",
        ),
        "1752132705",
    );
});


test("Binario convierte a hexadecimal", () => {
    assert.equal(
        binaryToHex(
            "01101000011011110110110001100001",
        ),
        "686f6c61",
    );
});


test("Análisis automático detecta Base64", () => {
    assert.deepEqual(
        smartDecode("aG9sYQ=="),
        {
            base64: "hola",
        },
    );
});


test("Análisis automático detecta hexadecimal", () => {
    assert.deepEqual(
        smartDecode("686f6c61"),
        {
            hex: "hola",
        },
    );
});


test("Análisis automático detecta URL", () => {
    assert.deepEqual(
        smartDecode("%68%6F%6C%61"),
        {
            url: "hola",
        },
    );
});


test("Análisis automático detecta binario", () => {
    assert.deepEqual(
        smartDecode(
            "01101000 01101111 01101100 01100001",
        ),
        {
            binaryText: "hola",
            binaryDecimal: "1752132705",
            binaryHex: "686f6c61",
        },
    );
});


test("Análisis automático no inventa ROT13", () => {
    assert.deepEqual(
        smartDecode("texto normal"),
        {},
    );
});


test("Formato inteligente informa ausencia", () => {
    const result = formatSmartResults({});

    assert.match(
        result,
        /No se detectó una codificación compatible/,
    );

    assert.match(
        result,
        /ROT13/,
    );
});


test("convertValue usa el mismo motor", () => {
    assert.equal(
        convertValue(
            "base64Encode",
            "Hackcop",
        ),
        "SGFja2NvcA==",
    );
});


test("convertValue rechaza modos desconocidos", () => {
    assert.throws(
        () => convertValue(
            "modoInexistente",
            "hola",
        ),
        /Modo desconocido/,
    );
});

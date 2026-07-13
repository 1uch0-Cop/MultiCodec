/**
 * Motor web de MultiCodec.
 *
 * Todas las conversiones se ejecutan localmente en el navegador.
 * No se transmiten datos a servicios externos.
 */

export const INVALID_BASE64 =
    "⚠️ Entrada Base64 inválida.";

export const INVALID_BASE64_TEXT =
    "⚠️ Base64 válido, pero el contenido no es texto UTF-8.";

export const INVALID_HEX =
    "⚠️ Entrada hexadecimal inválida.";

export const INVALID_HEX_TEXT =
    "⚠️ Hexadecimal válido, pero el contenido no es texto UTF-8.";

export const INVALID_BINARY =
    "⚠️ Secuencia binaria inválida.";

export const INVALID_BINARY_TEXT =
    "⚠️ Binario válido, pero el contenido no es texto UTF-8.";

export const INVALID_URL =
    "⚠️ Codificación URL inválida.";


const BASE64_PATTERN =
    /^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/;


function bytesToBase64(bytes) {
    if (typeof btoa === "function") {
        let binary = "";
        const chunkSize = 0x8000;

        for (
            let index = 0;
            index < bytes.length;
            index += chunkSize
        ) {
            const chunk = bytes.subarray(
                index,
                index + chunkSize,
            );

            binary += String.fromCharCode(...chunk);
        }

        return btoa(binary);
    }

    if (typeof Buffer !== "undefined") {
        return Buffer.from(bytes).toString("base64");
    }

    throw new Error(
        "El entorno no proporciona un codificador Base64.",
    );
}


function base64ToBytes(value) {
    if (typeof atob === "function") {
        const binary = atob(value);
        const bytes = new Uint8Array(binary.length);

        for (
            let index = 0;
            index < binary.length;
            index += 1
        ) {
            bytes[index] = binary.charCodeAt(index);
        }

        return bytes;
    }

    if (typeof Buffer !== "undefined") {
        return Uint8Array.from(
            Buffer.from(value, "base64"),
        );
    }

    throw new Error(
        "El entorno no proporciona un decodificador Base64.",
    );
}


function decodeUtf8(bytes, invalidMessage) {
    try {
        return new TextDecoder(
            "utf-8",
            { fatal: true },
        ).decode(bytes);
    } catch {
        return invalidMessage;
    }
}


function cleanBinary(value) {
    const compact = value.replace(/\s+/g, "");

    if (
        compact.length === 0
        || !/^[01]+$/.test(compact)
    ) {
        return null;
    }

    return compact;
}


export function encodeBase64(text) {
    const bytes = new TextEncoder().encode(text);

    return bytesToBase64(bytes);
}


export function decodeBase64(text) {
    const compact = text.replace(/\s+/g, "");

    if (compact === "") {
        return "";
    }

    if (
        compact.length % 4 !== 0
        || !BASE64_PATTERN.test(compact)
    ) {
        return INVALID_BASE64;
    }

    try {
        const decoded = base64ToBytes(compact);

        return decodeUtf8(
            decoded,
            INVALID_BASE64_TEXT,
        );
    } catch {
        return INVALID_BASE64;
    }
}


export function encodeHex(text) {
    const bytes = new TextEncoder().encode(text);

    return Array.from(
        bytes,
        byte => byte.toString(16).padStart(2, "0"),
    ).join("");
}


export function decodeHex(text) {
    const compact = text.replace(/\s+/g, "");

    if (compact === "") {
        return "";
    }

    if (
        compact.length % 2 !== 0
        || !/^[0-9A-Fa-f]+$/.test(compact)
    ) {
        return INVALID_HEX;
    }

    const bytes = new Uint8Array(
        compact.length / 2,
    );

    for (
        let index = 0;
        index < compact.length;
        index += 2
    ) {
        bytes[index / 2] = Number.parseInt(
            compact.slice(index, index + 2),
            16,
        );
    }

    return decodeUtf8(
        bytes,
        INVALID_HEX_TEXT,
    );
}


export function rot13(text) {
    return text.replace(
        /[A-Za-z]/g,
        character => {
            const code = character.charCodeAt(0);
            const base = code <= 90 ? 65 : 97;

            return String.fromCharCode(
                (
                    (code - base + 13)
                    % 26
                ) + base,
            );
        },
    );
}


export function encodeUrl(text) {
    try {
        return encodeURIComponent(text).replace(
            /[!'()*]/g,
            character => (
                `%${character
                    .charCodeAt(0)
                    .toString(16)
                    .toUpperCase()}`
            ),
        );
    } catch {
        return INVALID_URL;
    }
}


export function decodeUrl(text) {
    if (/%(?![0-9A-Fa-f]{2})/.test(text)) {
        return INVALID_URL;
    }

    try {
        return decodeURIComponent(text);
    } catch {
        return INVALID_URL;
    }
}


export function textToBinary(text) {
    const bytes = new TextEncoder().encode(text);

    return Array.from(
        bytes,
        byte => byte.toString(2).padStart(8, "0"),
    ).join(" ");
}


export function binaryToText(binary) {
    const compact = cleanBinary(binary);

    if (
        compact === null
        || compact.length % 8 !== 0
    ) {
        return INVALID_BINARY;
    }

    const bytes = new Uint8Array(
        compact.length / 8,
    );

    for (
        let index = 0;
        index < compact.length;
        index += 8
    ) {
        bytes[index / 8] = Number.parseInt(
            compact.slice(index, index + 8),
            2,
        );
    }

    return decodeUtf8(
        bytes,
        INVALID_BINARY_TEXT,
    );
}


export function binaryToDecimal(binary) {
    const compact = cleanBinary(binary);

    if (compact === null) {
        return INVALID_BINARY;
    }

    return BigInt(`0b${compact}`).toString(10);
}


export function binaryToHex(binary) {
    const compact = cleanBinary(binary);

    if (compact === null) {
        return INVALID_BINARY;
    }

    return BigInt(`0b${compact}`).toString(16);
}


export function looksLikeBinary(value) {
    const compact = cleanBinary(value);

    return (
        compact !== null
        && compact.length % 8 === 0
    );
}


export function looksLikeHex(value) {
    const compact = value.replace(/\s+/g, "");

    return (
        compact.length > 0
        && compact.length % 2 === 0
        && /^[0-9A-Fa-f]+$/.test(compact)
    );
}


export function looksLikeBase64(value) {
    const compact = value.replace(/\s+/g, "");

    return (
        compact.length > 0
        && compact.length % 4 === 0
        && BASE64_PATTERN.test(compact)
    );
}


export function looksLikeUrlEncoding(value) {
    return /%[0-9A-Fa-f]{2}/.test(value);
}


export function isReadableText(text) {
    if (text.length === 0) {
        return false;
    }

    const characters = Array.from(text);

    const readable = characters.filter(
        character => {
            const code = character.codePointAt(0);

            return (
                code === 9
                || code === 10
                || code === 13
                || (
                    code >= 32
                    && !(code >= 127 && code <= 159)
                )
            );
        },
    ).length;

    return readable / characters.length >= 0.85;
}


export function smartDecode(value) {
    const results = {};

    if (looksLikeBase64(value)) {
        const decoded = decodeBase64(value);

        if (
            !decoded.startsWith("⚠️")
            && isReadableText(decoded)
        ) {
            results.base64 = decoded;
        }
    }

    if (looksLikeHex(value)) {
        const decoded = decodeHex(value);

        if (
            !decoded.startsWith("⚠️")
            && isReadableText(decoded)
        ) {
            results.hex = decoded;
        }
    }

    if (looksLikeUrlEncoding(value)) {
        const decoded = decodeUrl(value);

        if (
            decoded !== value
            && !decoded.startsWith("⚠️")
            && isReadableText(decoded)
        ) {
            results.url = decoded;
        }
    }

    if (looksLikeBinary(value)) {
        const decodedText = binaryToText(value);

        if (
            !decodedText.startsWith("⚠️")
            && isReadableText(decodedText)
        ) {
            results.binaryText = decodedText;
        }

        results.binaryDecimal =
            binaryToDecimal(value);

        results.binaryHex =
            binaryToHex(value);
    }

    return results;
}


export function formatSmartResults(results) {
    const labels = {
        base64: "Base64",
        hex: "Hexadecimal",
        url: "URL",
        binaryText: "Binario → Texto",
        binaryDecimal: "Binario → Decimal",
        binaryHex: "Binario → Hexadecimal",
    };

    const entries = Object.entries(results);

    if (entries.length === 0) {
        return [
            "No se detectó una codificación compatible.",
            "",
            "Nota: ROT13 no puede identificarse de manera",
            "fiable y debe probarse manualmente.",
        ].join("\n");
    }

    return entries.map(
        ([formatName, result]) => (
            `[${labels[formatName] ?? formatName}]\n`
            + result
        ),
    ).join("\n\n");
}


export function convertValue(mode, value) {
    const actions = {
        base64Encode: encodeBase64,
        base64Decode: decodeBase64,
        hexEncode: encodeHex,
        hexDecode: decodeHex,
        rot13Encode: rot13,
        rot13Decode: rot13,
        urlEncode: encodeUrl,
        urlDecode: decodeUrl,
        binaryEncode: textToBinary,
        binaryDecode: binaryToText,
        binaryDecimal: binaryToDecimal,
        binaryHex: binaryToHex,
    };

    if (mode === "smart") {
        return formatSmartResults(
            smartDecode(value),
        );
    }

    const action = actions[mode];

    if (action === undefined) {
        throw new Error(
            `Modo desconocido: ${mode}`,
        );
    }

    return action(value);
}

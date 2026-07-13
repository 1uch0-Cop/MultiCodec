import {
    convertValue,
} from "./multicodec.js";


const modeSelect = document.querySelector("#mode");
const inputArea = document.querySelector("#input");
const outputArea = document.querySelector("#output");
const convertButton = document.querySelector("#convert");
const clearButton = document.querySelector("#clear");
const copyButton = document.querySelector("#copy");
const statusMessage = document.querySelector("#status");
const inputCount = document.querySelector("#input-count");
const outputCount = document.querySelector("#output-count");


function setStatus(message, type = "info") {
    statusMessage.textContent = message;
    statusMessage.dataset.type = type;
}


function updateCounters() {
    inputCount.textContent =
        `${inputArea.value.length} caracteres`;

    outputCount.textContent =
        `${outputArea.value.length} caracteres`;
}


function convert() {
    const value = inputArea.value;

    if (value === "") {
        outputArea.value = "";
        updateCounters();

        setStatus(
            "Ingresa un valor antes de convertir.",
            "warning",
        );

        inputArea.focus();
        return;
    }

    try {
        outputArea.value = convertValue(
            modeSelect.value,
            value,
        );

        updateCounters();

        setStatus(
            "Conversión completada localmente.",
            "success",
        );
    } catch (error) {
        outputArea.value =
            `⚠️ Error inesperado: ${error.message}`;

        updateCounters();

        setStatus(
            "La conversión no pudo completarse.",
            "error",
        );
    }
}


function clearFields() {
    inputArea.value = "";
    outputArea.value = "";

    updateCounters();

    setStatus("Campos limpiados.");
    inputArea.focus();
}


async function copyOutput() {
    if (outputArea.value === "") {
        setStatus(
            "No hay contenido para copiar.",
            "warning",
        );
        return;
    }

    try {
        await navigator.clipboard.writeText(
            outputArea.value,
        );

        setStatus(
            "Salida copiada al portapapeles.",
            "success",
        );
    } catch {
        outputArea.select();

        const copied = document.execCommand("copy");

        setStatus(
            copied
                ? "Salida copiada al portapapeles."
                : "No fue posible copiar la salida.",
            copied ? "success" : "error",
        );
    }
}


convertButton.addEventListener("click", convert);
clearButton.addEventListener("click", clearFields);
copyButton.addEventListener("click", copyOutput);

inputArea.addEventListener(
    "input",
    updateCounters,
);

outputArea.addEventListener(
    "input",
    updateCounters,
);

document.addEventListener(
    "keydown",
    event => {
        if (
            event.ctrlKey
            && event.key === "Enter"
        ) {
            event.preventDefault();
            convert();
        }
    },
);

updateCounters();
inputArea.focus();

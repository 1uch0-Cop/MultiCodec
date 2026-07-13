#!/usr/bin/env python3
"""Interfaz gráfica de MultiCodec basada en Tkinter."""

from __future__ import annotations

import tkinter as tk
from tkinter import scrolledtext, ttk

import converter


MODE_OPTIONS: tuple[tuple[str, str], ...] = (
    ("Texto → Base64", "base64_encode"),
    ("Base64 → Texto", "base64_decode"),
    ("Texto → Hexadecimal", "hex_encode"),
    ("Hexadecimal → Texto", "hex_decode"),
    ("Texto → ROT13", "rot13_encode"),
    ("ROT13 → Texto", "rot13_decode"),
    ("Texto → URL", "url_encode"),
    ("URL → Texto", "url_decode"),
    ("Texto → Binario UTF-8", "binary_encode"),
    ("Binario UTF-8 → Texto", "binary_decode"),
    ("Binario → Decimal", "binary_decimal"),
    ("Binario → Hexadecimal", "binary_hex"),
    ("Análisis automático", "smart"),
)

MODE_LABELS = {
    mode_code: label
    for label, mode_code in MODE_OPTIONS
}

SMART_LABELS = {
    "base64": "Base64",
    "hex": "Hexadecimal",
    "url": "URL",
    "binary_text": "Binario → Texto",
    "binary_decimal": "Binario → Decimal",
    "binary_hex": "Binario → Hexadecimal",
}


def format_smart_results(results: dict[str, str]) -> str:
    """Prepara los resultados de detección automática."""
    if not results:
        return (
            "No se detectó una codificación compatible.\n\n"
            "Nota: ROT13 no puede identificarse de manera "
            "fiable y debe probarse manualmente."
        )

    sections = []

    for format_name, value in results.items():
        visible_name = SMART_LABELS.get(
            format_name,
            format_name,
        )
        sections.append(f"[{visible_name}]\n{value}")

    return "\n\n".join(sections)


def convert_value(mode: str, value: str) -> str:
    """Ejecuta una conversión sin depender de la ventana."""
    actions = {
        "base64_encode": converter.encode_base64,
        "base64_decode": converter.decode_base64,
        "hex_encode": converter.encode_hex,
        "hex_decode": converter.decode_hex,
        "rot13_encode": converter.encode_rot13,
        "rot13_decode": converter.decode_rot13,
        "url_encode": converter.encode_url,
        "url_decode": converter.decode_url,
        "binary_encode": converter.text_to_binary,
        "binary_decode": converter.binary_to_text,
        "binary_decimal": converter.binary_to_decimal,
        "binary_hex": converter.binary_to_hex,
    }

    if mode == "smart":
        return format_smart_results(
            converter.smart_decode(value)
        )

    action = actions.get(mode)

    if action is None:
        raise ValueError(f"Modo desconocido: {mode}")

    return action(value)


class MultiCodecApp(ttk.Frame):
    """Aplicación gráfica principal."""

    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master, padding=16)

        self.master = master
        self.mode_var = tk.StringVar(
            value=MODE_OPTIONS[0][0]
        )
        self.status_var = tk.StringVar(
            value="Listo."
        )

        self._configure_window()
        self._build_widgets()
        self._bind_shortcuts()

    def _configure_window(self) -> None:
        """Configura tamaño y comportamiento de la ventana."""
        self.master.title("MultiCodec")
        self.master.geometry("820x620")
        self.master.minsize(620, 480)

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        self.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(7, weight=1)

    def _build_widgets(self) -> None:
        """Construye los controles de la interfaz."""
        title = ttk.Label(
            self,
            text="MultiCodec",
            font=("", 18, "bold"),
        )
        title.grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 4),
        )

        subtitle = ttk.Label(
            self,
            text=(
                "Herramienta educativa para codificación "
                "y representación de datos"
            ),
        )
        subtitle.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(0, 14),
        )

        mode_frame = ttk.Frame(self)
        mode_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, 10),
        )
        mode_frame.columnconfigure(1, weight=1)

        ttk.Label(
            mode_frame,
            text="Conversión:",
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 10),
        )

        self.mode_combo = ttk.Combobox(
            mode_frame,
            textvariable=self.mode_var,
            values=[
                label
                for label, _ in MODE_OPTIONS
            ],
            state="readonly",
        )
        self.mode_combo.grid(
            row=0,
            column=1,
            sticky="ew",
        )
        self.mode_combo.current(0)

        input_frame = ttk.LabelFrame(
            self,
            text="Entrada",
            padding=8,
        )
        input_frame.grid(
            row=3,
            column=0,
            sticky="nsew",
            pady=(0, 10),
        )
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)

        self.input_box = scrolledtext.ScrolledText(
            input_frame,
            wrap=tk.WORD,
            undo=True,
            font=("monospace", 11),
        )
        self.input_box.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        button_frame = ttk.Frame(self)
        button_frame.grid(
            row=4,
            column=0,
            sticky="ew",
            pady=(0, 10),
        )
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)

        ttk.Button(
            button_frame,
            text="Convertir",
            command=self.convert,
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 5),
        )

        ttk.Button(
            button_frame,
            text="Limpiar",
            command=self.clear,
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5,
        )

        ttk.Button(
            button_frame,
            text="Copiar salida",
            command=self.copy_output,
        ).grid(
            row=0,
            column=2,
            sticky="ew",
            padx=(5, 0),
        )

        shortcut_label = ttk.Label(
            self,
            text="Atajo: Ctrl+Enter para convertir",
        )
        shortcut_label.grid(
            row=5,
            column=0,
            sticky="w",
            pady=(0, 8),
        )

        output_frame = ttk.LabelFrame(
            self,
            text="Salida",
            padding=8,
        )
        output_frame.grid(
            row=7,
            column=0,
            sticky="nsew",
        )
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

        self.output_box = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=("monospace", 11),
            state=tk.DISABLED,
        )
        self.output_box.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        status = ttk.Label(
            self,
            textvariable=self.status_var,
            anchor="w",
        )
        status.grid(
            row=8,
            column=0,
            sticky="ew",
            pady=(8, 0),
        )

        self.input_box.focus_set()

    def _bind_shortcuts(self) -> None:
        """Registra atajos de teclado."""
        self.master.bind(
            "<Control-Return>",
            self._convert_from_event,
        )

    def _selected_mode(self) -> str:
        """Obtiene el código interno del modo seleccionado."""
        selected_label = self.mode_var.get()

        for label, mode_code in MODE_OPTIONS:
            if label == selected_label:
                return mode_code

        raise ValueError(
            f"Modo visual desconocido: {selected_label}"
        )

    def _set_output(self, value: str) -> None:
        """Actualiza de forma controlada el área de salida."""
        self.output_box.configure(state=tk.NORMAL)
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert("1.0", value)
        self.output_box.configure(state=tk.DISABLED)

    def _convert_from_event(
        self,
        _event: tk.Event,
    ) -> str:
        """Permite ejecutar la conversión desde el teclado."""
        self.convert()
        return "break"

    def convert(self) -> None:
        """Convierte la entrada usando el modo seleccionado."""
        value = self.input_box.get(
            "1.0",
            "end-1c",
        )

        if value == "":
            self._set_output("")
            self.status_var.set(
                "Ingresa un valor antes de convertir."
            )
            return

        try:
            mode = self._selected_mode()
            result = convert_value(mode, value)
        except Exception as error:
            self._set_output(
                f"⚠️ Error inesperado: {error}"
            )
            self.status_var.set(
                "La conversión no pudo completarse."
            )
            return

        self._set_output(result)
        self.status_var.set(
            f"Conversión completada: {MODE_LABELS[mode]}."
        )

    def clear(self) -> None:
        """Limpia la entrada y la salida."""
        self.input_box.delete("1.0", tk.END)
        self._set_output("")
        self.status_var.set("Campos limpiados.")
        self.input_box.focus_set()

    def copy_output(self) -> None:
        """Copia el resultado al portapapeles."""
        value = self.output_box.get(
            "1.0",
            "end-1c",
        )

        if value == "":
            self.status_var.set(
                "No hay contenido para copiar."
            )
            return

        self.master.clipboard_clear()
        self.master.clipboard_append(value)
        self.master.update_idletasks()

        self.status_var.set(
            "Salida copiada al portapapeles."
        )


def main() -> None:
    """Inicia MultiCodec en modo gráfico."""
    root = tk.Tk()
    MultiCodecApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

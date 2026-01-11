#!/usr/bin/env python3
# GUI simple para Text Converter Tool

import tkinter as tk
from tkinter import ttk, scrolledtext
import converter


MODES = [
    ("Text → Base64", "b64e"),
    ("Base64 → Text", "b64d"),
    ("Text → Hex", "hexe"),
    ("Hex → Text", "hexd"),
    ("Text → ROT13", "rot13e"),
    ("ROT13 → Text", "rot13d"),
    ("Text → URL", "urle"),
    ("URL → Text", "urld"),
    ("Text → Binary", "t2b"),
    ("Binary → Text", "b2t"),
    ("Binary → Decimal", "b2d"),
    ("Binary → Hex", "b2h"),
    ("Smart Decode (Forense)", "smart"),
]


def convert_action():
    mode = mode_var.get()
    text = input_box.get("1.0", tk.END).strip()
    if not text:
        output_box.delete("1.0", tk.END)
        return

    if mode == "b64e":
        out = converter.encode_base64(text)
    elif mode == "b64d":
        out = converter.decode_base64(text)
    elif mode == "hexe":
        out = converter.encode_hex(text)
    elif mode == "hexd":
        out = converter.decode_hex(text)
    elif mode == "rot13e":
        out = converter.encode_rot13(text)
    elif mode == "rot13d":
        out = converter.decode_rot13(text)
    elif mode == "urle":
        out = converter.encode_url(text)
    elif mode == "urld":
        out = converter.decode_url(text)
    elif mode == "t2b":
        out = converter.text_to_binary(text)
    elif mode == "b2t":
        out = converter.binary_to_text(text)
    elif mode == "b2d":
        out = converter.binary_to_decimal(text)
    elif mode == "b2h":
        out = converter.binary_to_hex(text)
    elif mode == "smart":
        res = converter.smart_decode(text)
        if not res:
            out = "No se detectó ningún formato claro."
        else:
            out_lines = []
            for k, v in res.items():
                out_lines.append(f"[{k}]\n{v}")
            out = "\n\n".join(out_lines)
    else:
        out = ""

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, out)


root = tk.Tk()
root.title("Text Converter Tool – GUI")

main_frame = ttk.Frame(root, padding=10)
main_frame.grid(sticky="nsew")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(2, weight=1)
main_frame.rowconfigure(4, weight=1)

ttk.Label(main_frame, text="Modo:").grid(row=0, column=0, sticky="w")

mode_var = tk.StringVar(value="b64e")
mode_combo = ttk.Combobox(
    main_frame,
    textvariable=mode_var,
    values=[m[0] for m in MODES],
    state="readonly",
)
mode_combo.grid(row=1, column=0, sticky="ew", pady=(0, 8))


def on_mode_change(event):
    idx = mode_combo.current()
    if idx >= 0:
        mode_var.set(MODES[idx][1])


mode_combo.bind("<<ComboboxSelected>>", on_mode_change)

ttk.Label(main_frame, text="Entrada:").grid(row=2, column=0, sticky="w")
input_box = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=6)
input_box.grid(row=3, column=0, sticky="nsew", pady=(0, 8))

convert_btn = ttk.Button(main_frame, text="Convertir", command=convert_action)
convert_btn.grid(row=4, column=0, sticky="ew", pady=(0, 8))

ttk.Label(main_frame, text="Salida:").grid(row=5, column=0, sticky="w")
output_box = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=6)
output_box.grid(row=6, column=0, sticky="nsew")

root.mainloop()

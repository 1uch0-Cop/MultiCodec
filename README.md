# Text Converter Tool

Herramienta de línea de comandos para convertir texto entre múltiples formatos de codificación. Pensada para aprendizaje de ciberseguridad, CTF, análisis forense básico y experimentación con representaciones de datos (texto, binario, hexadecimal, Base64, ROT13 y URL encoding).

Autor: **1uch0 @2025**

---

## ✨ Funcionalidades

Conversión entre:

- **Base64**
  - `Text → Base64`
  - `Base64 → Text`
- **Hexadecimal**
  - `Text → Hex`
  - `Hex → Text`
- **ROT13**
  - `Encode / Decode`
- **URL encoding**
  - `Encode / Decode`
- **Binario**
  - `Text → Binary` (8 bits por carácter)
  - `Binary → Text`
  - `Binary → Decimal`
  - `Binary → Hex`
- **Modo forense (Smart Decode)**
  - Intenta detectar automáticamente si la entrada es:
    - Base64
    - Hex
    - Binario
    - URL encoded
    - ROT13
  - Devuelve todos los decodificados posibles.

---

## 🧩 Estructura del proyecto

```text
.
├─ converter.py          # CLI principal
├─ gui.py                # Interfaz gráfica (Tkinter)
├─ index.html            # Versión web estática (HTML+JS)
├─ requirements.txt      # Dependencias Python
└─ tests/
   └─ test_converter.py  # Pruebas unitarias (pytest)

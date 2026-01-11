# MultiCodec

**MultiCodec** es una herramienta educativa para conversión de texto entre múltiples formatos de codificación. Útil en ciberseguridad, CTF, análisis forense, OSINT, y clases de representación de datos.

Autor: **1uch0 @2025**

---

## ✨ Funcionalidades

Conversión entre:

- **Base64**
  - Text → Base64
  - Base64 → Text
- **Hexadecimal**
  - Text → Hex
  - Hex → Text
- **ROT13**
  - Encode / Decode
- **URL encoding**
  - Encode / Decode
- **Binario**
  - Text → Binary (8 bits por carácter)
  - Binary → Text
  - Binary → Decimal
  - Binary → Hex
- **Modo Forense (Smart Decode)**
  Detecta posibles codificaciones en una cadena sospechosa y las decodifica si es posible:
  - Base64
  - Hex
  - Binary
  - URL
  - ROT13

---

## 🧩 Estructura del Proyecto

```text
MultiCodec/
├─ converter.py          # CLI principal
├─ gui.py                # Interfaz gráfica (Tkinter)
├─ index.html            # Versión web estática (HTML+JS)
├─ requirements.txt      # Dependencias Python (mínimas)
└─ tests/
   └─ test_converter.py  # Pruebas unitarias (pytest)

Uso (CLI)
Ejecuta:
python3 converter.py

Menú interactivo:
=== TEXT CONVERTER TOOL ===
1. Encode Base64
2. Decode Base64
3. Encode Hex
4. Decode Hex
5. Encode ROT13
6. Decode ROT13
7. Encode URL
8. Decode URL
9. Text → Binary
10. Binary → Text
11. Binary → Decimal
12. Binary → Hex
13. Smart Decode (Forense)
14. Exit

Versión Web (HTML + JS)
La versión web se encuentra en index.html.
Opciones:
abrir directamente (offline), o
publicar en GitHub Pages:
Instrucciones:
Ir a: Settings → Pages
Source: main — /root
Guardar

Pruebas Unitarias
Requiere pytest.
pip install -r requirements.txt
pytest

Pruebas incluidas para:
Base64 (roundtrip)
Hex (roundtrip)
ROT13
Text ↔ Binary
Binary → Decimal / Hex
Smart Decode para formatos comunes
Interfaz Gráfica (GUI)
Archivo: gui.py
Usa Tkinter, incluido en Python estándar.
Permite elegir modo, ingresar texto y ver resultado en tiempo real. Ideal para uso en sala de computación.
Modo Forense (Smart Decode)
Perfecto para payloads en CTF, correos sospechosos o cadenas pegadas desde logs.
Ejemplo de salida:
[Base64]
hola
[Hex → Text]
hola
[Binary → Text]
hola
Instalación
git clone https://github.com/TU-USUARIO/MultiCodec.git
cd MultiCodec
pip install -r requirements.txt
Roadmap
Características planeadas:
Hashing (MD5, SHA1, SHA256)
Smart multi-decode recursivo (detecta capas)
Exportar resultados JSON/CSV
Integración con clipboard
Versión Web avanzada con historial
WebAssembly para rendimiento
Licencia
Uso educativo. Puedes adaptar y reutilizar citando al autor 1uch0 @2025.

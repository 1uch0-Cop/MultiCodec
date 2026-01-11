# Text Converter Tool

Herramienta de línea de comandos para convertir texto entre múltiples formatos de codificación. Pensada para aprendizaje de ciberseguridad, CTF, análisis forense básico y experimentación con representaciones de datos (texto, binario, hexadecimal, Base64, ROT13 y URL encoding).

Autor: **1uch0 @2025**

---

## Funcionalidades

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

## Estructura del proyecto

```text
.
├─ converter.py          # CLI principal
├─ gui.py                # Interfaz gráfica (Tkinter)
├─ index.html            # Versión web estática (HTML+JS)
├─ requirements.txt      # Dependencias Python
└─ tests/
   └─ test_converter.py  # Pruebas unitarias (pytest)

Uso (CLI)
Ejecutar:
python converter.py

Menú principal:

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


Ejemplo: Text → Hex

Opción 3

Texto: hola

Resultado: 686f6c61

Ejemplo: Binary → Hex

Opción 12

Binario: 01101000 01101111 01101100 01100001

Resultado: 686f6c61

Versión Web (estática)

El archivo index.html contiene una versión 100% estática (HTML + CSS + JS):

Funciona directamente en el navegador (doble clic en index.html).

No requiere Python ni servidor.

Ideal para subir a GitHub Pages o usar en clases.

Pruebas

Se incluye un archivo de pruebas con pytest:

pip install -r requirements.txt
pytest


Las pruebas validan el comportamiento básico de:

Base64

Hex

ROT13

Binario ↔ Texto

Binario → Decimal / Hex

Modo Forense (Smart Decode)

El modo forense intenta adivinar el tipo de codificación de una cadena dada y muestra todos los decodificados posibles.

Ejemplo de uso:

Seleccionar opción 13 en el menú.

Pegar una cadena sospechosa (por ejemplo, de un correo, payload, CTF).

Revisar las posibles decodificaciones sugeridas.

Interfaz Gráfica (GUI)

Archivo: gui.py

Usa Tkinter (incluido en Python estándar).

Permite:

Escribir un texto

Elegir tipo de conversión

Ver el resultado en un cuadro de texto

Pensado para demostraciones rápidas en laboratorio.

Instalación

Clonar el repositorio:

git clone https://github.com/TU-USUARIO/TU-REPO.git
cd TU-REPO


Instalar dependencias (mínimas):

pip install -r requirements.txt

Roadmap

Ideas futuras:

Detección automática multi-etapa (encode anidado).

Hashing (MD5, SHA-1, SHA-256).

Integración con módulos de análisis forense.

Versión web mejorada con historial y exportación.

Licencia

Uso educativo. Puedes adaptar y reutilizar el código citando al autor original (1uch0 @2025) y enlazando el repositorio.

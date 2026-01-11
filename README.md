Text Converter Tool

Utilidad de línea de comandos para convertir texto entre distintos formatos de codificación, ideal para estudiantes, entusiastas de CTF, forenses digitales y pentesters que necesitan manipular representación de datos a bajo nivel (binario, hexadecimal, ROT13, Base64 y URL encoding).

Características

El programa actualmente soporta:

Base64

Encode → Text → Base64

Decode → Base64 → Text

Hexadecimal

Encode → Text → Hex

Decode → Hex → Text

ROT13

Encode / Decode

URL Encoding

Encode / Decode

Binario

Text → Binary

Binary → Text

Binary → Decimal

Binary → Hex

Uso

Ejecutar desde consola:

python3 converter.py


y seleccionar una opción del menú interactivo.

Ejemplo real:

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
13. Exit

Dependencias

Todas las dependencias son estándar de Python:

import base64
import codecs
import urllib.parse


No requiere instalación adicional.

Ejemplos rápidos
Texto → Hex

Entrada:

hola


Salida:

686f6c61

Binario → Hex

Entrada:

01101000 01101111 01101100 01100001


Salida:

686f6c61

Hex → Texto

Entrada:

686f6c61


Salida:

hola

Validaciones implementadas

Decodificación segura para evitar crashes

Mensajes cuando la entrada no tiene longitud válida (Base64)

Manejo de excepciones (hex inválido, binario inválido, URL malformed, etc.)

Ejemplo:

⚠️ Invalid Base64 input (length must be multiple of 4).

Público objetivo

Estudiantes de ciberseguridad

Participantes de CTF

Docentes que explican representación de datos

Analistas forenses

Programadores que manipulan encoding básico

OSINT / Blue Team que requieren decodificar cadenas sospechosas

Roadmap

Oportunidades futuras:

GUI con Tkinter o PyQt

Modo API para automatización

Exportar resultados a JSON

Integración con hashing (MD5, SHA-1, SHA-256)

Decodificación inteligente de payloads (detect Base64 / Hex / URL / ROT13 automáticamente)

Versión Web en JavaScript para Chrome/Firefox



Autoría

Proyecto por 1uch0 (2025).
Creado inicialmente como herramienta educativa para manipulación básica de datos en contextos de ciberseguridad.

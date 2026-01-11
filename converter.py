
---

## 2. `converter.py` (código refactorizado + modo forense)

```python
#!/usr/bin/env python3
# 1uch0 @2025

import base64
import codecs
import urllib.parse


def menu() -> None:
    print("\n=== TEXT CONVERTER TOOL ===")
    print("1. Encode Base64")
    print("2. Decode Base64")
    print("3. Encode Hex")
    print("4. Decode Hex")
    print("5. Encode ROT13")
    print("6. Decode ROT13")
    print("7. Encode URL")
    print("8. Decode URL")
    print("9. Text → Binary")
    print("10. Binary → Text")
    print("11. Binary → Decimal")
    print("12. Binary → Hex")
    print("13. Smart Decode (Forense)")
    print("14. Exit")


# --- Funciones de codificación/decodificación --- #

def encode_base64(text: str) -> str:
    return base64.b64encode(text.encode()).decode()


def decode_base64(text: str) -> str:
    try:
        if len(text) % 4 != 0:
            return "⚠️ Invalid Base64 input (length must be multiple of 4)."
        return base64.b64decode(text.encode()).decode(errors="ignore")
    except Exception:
        return "⚠️ Invalid Base64 input."


def encode_hex(text: str) -> str:
    return text.encode().hex()


def decode_hex(text: str) -> str:
    try:
        return bytes.fromhex(text).decode(errors="ignore")
    except Exception:
        return "⚠️ Invalid Hex input."


def encode_rot13(text: str) -> str:
    return codecs.encode(text, "rot_13")


def decode_rot13(text: str) -> str:
    try:
        return codecs.decode(text, "rot_13")
    except Exception:
        return "⚠️ Invalid ROT13 input."


def encode_url(text: str) -> str:
    return urllib.parse.quote(text)


def decode_url(text: str) -> str:
    try:
        return urllib.parse.unquote(text)
    except Exception:
        return "⚠️ Invalid URL input."


def text_to_binary(text: str) -> str:
    return " ".join(format(ord(char), "08b") for char in text)


def binary_to_text(binary: str) -> str:
    try:
        return "".join(chr(int(b, 2)) for b in binary.split())
    except Exception:
        return "⚠️ Invalid binary sequence."


def binary_to_decimal(binary: str) -> str:
    try:
        return str(int(binary.replace(" ", ""), 2))
    except Exception:
        return "⚠️ Invalid binary number."


def binary_to_hex(binary: str) -> str:
    try:
        return hex(int(binary.replace(" ", ""), 2))[2:]
    except Exception:
        return "⚠️ Invalid binary number."


# --- Modo Forense: detección automática --- #

def looks_like_binary(s: str) -> bool:
    allowed = {"0", "1", " ", "\t"}
    return all(c in allowed for c in s) and any(c in {"0", "1"} for c in s)


def looks_like_hex(s: str) -> bool:
    s_clean = s.replace(" ", "")
    if len(s_clean) == 0 or len(s_clean) % 2 != 0:
        return False
    try:
        int(s_clean, 16)
        return True
    except ValueError:
        return False


def looks_like_base64(s: str) -> bool:
    s_clean = s.replace("\n", "").replace(" ", "")
    if len(s_clean) == 0 or len(s_clean) % 4 != 0:
        return False
    allowed = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    return all(c in allowed for c in s_clean)


def smart_decode(value: str) -> dict:
    """
    Intenta decodificar 'value' como varios formatos y devuelve un dict con resultados.
    No lanza excepciones, solo añade entradas cuando tiene sentido.
    """
    results = {}

    # Base64
    if looks_like_base64(value):
        results["base64"] = decode_base64(value)

    # Hex
    if looks_like_hex(value):
        results["hex"] = decode_hex(value)

    # URL
    if "%" in value or "+" in value:
        results["url"] = decode_url(value)

    # Binario
    if looks_like_binary(value):
        results["binary_text"] = binary_to_text(value)
        results["binary_decimal"] = binary_to_decimal(value)
        results["binary_hex"] = binary_to_hex(value)

    # ROT13 (se prueba siempre)
    rot13_decoded = decode_rot13(value)
    results["rot13"] = rot13_decoded

    return results


def run_smart_decode() -> None:
    value = input("Texto / cadena sospechosa a analizar: ")
    results = smart_decode(value)
    if not results:
        print("\nNo se detectó ningún formato claro. Revisa manualmente.")
        return

    print("\n=== Resultados Smart Decode ===")
    for fmt, decoded in results.items():
        print(f"\n[{fmt}]")
        print(decoded)


# --- Programa principal --- #

def main() -> None:
    while True:
        menu()
        option = input("\nChoose an option: ").strip()

        if option == "1":
            text = input("Text to encode in Base64: ")
            print("Encoded:", encode_base64(text))
        elif option == "2":
            text = input("Text in Base64 to decode: ")
            print("Decoded:", decode_base64(text))
        elif option == "3":
            text = input("Text to encode in Hex: ")
            print("Encoded:", encode_hex(text))
        elif option == "4":
            text = input("Text in Hex to decode: ")
            print("Decoded:", decode_hex(text))
        elif option == "5":
            text = input("Text to encode in ROT13: ")
            print("Encoded:", encode_rot13(text))
        elif option == "6":
            text = input("Text in ROT13 to decode: ")
            print("Decoded:", decode_rot13(text))
        elif option == "7":
            text = input("Text to encode in URL: ")
            print("Encoded:", encode_url(text))
        elif option == "8":
            text = input("Text in URL to decode: ")
            print("Decoded:", decode_url(text))
        elif option == "9":
            text = input("Text to convert to binary: ")
            print("Binary:", text_to_binary(text))
        elif option == "10":
            binary = input("Binary (space-separated) to convert to text: ")
            print("Text:", binary_to_text(binary))
        elif option == "11":
            binary = input("Binary number to convert to decimal: ")
            print("Decimal:", binary_to_decimal(binary))
        elif option == "12":
            binary = input("Binary number to convert to hex: ")
            print("Hexadecimal:", binary_to_hex(binary))
        elif option == "13":
            run_smart_decode()
        elif option == "14":
            print("Exiting... 👋")
            break
        else:
            print("❌ Invalid option, try again.")


if __name__ == "__main__":
    main()

#1uch0 @2025
# Multi-Decoder Python | Herramienta en Python para codificar y decodificar mensajes con varios métodos comunes en CTF y programación:

import base64
import binascii
import codecs
import urllib.parse

# ----- Funciones de codificación/decodificación -----
def encode_base64(text):
    return base64.b64encode(text.encode()).decode()

def decode_base64(text):
    try:
        return base64.b64decode(text.encode()).decode()
    except Exception:
        return "❌ Invalid Base64 input"

def encode_hex(text):
    return binascii.hexlify(text.encode()).decode()

def decode_hex(text):
    try:
        return binascii.unhexlify(text.encode()).decode()
    except Exception:
        return "❌ Invalid Hex input"

def encode_rot13(text):
    return codecs.encode(text, 'rot_13')

def decode_rot13(text):
    return codecs.decode(text, 'rot_13')

def encode_url(text):
    return urllib.parse.quote(text)

def decode_url(text):
    return urllib.parse.unquote(text)

# ----- Menú interactivo -----
def menu():
    print("\n=== Python Multi-Decoder ===")
    print("1. Encode to Base64")
    print("2. Decode from Base64")
    print("3. Encode to Hex (Binascii)")
    print("4. Decode from Hex (Binascii)")
    print("5. Encode to ROT13")
    print("6. Decode from ROT13")
    print("7. Encode to URL")
    print("8. Decode from URL")
    print("9. Exit")

# ----- Función principal -----
def main():
    while True:
        menu()
        option = input("\nChoose an option: ")

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
            print("Exiting... 👋")
            break

        else:
            print("❌ Invalid option, try again.")

# ----- Ejecutar script -----
if __name__ == "__main__":
    main()

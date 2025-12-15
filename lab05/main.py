import hashlib
import base64
from pathlib import Path

# Генерація симетричного ключа з персональних даних
def derive_key(personal: str, length: int = 32) -> bytes:
    digest = hashlib.sha256(personal.encode("utf-8")).digest()
    return digest[:length]

# XOR-шифрування/дешифрування байтів
def xor_bytes(data: bytes, key: bytes) -> bytes:
    result = bytearray(len(data))
    for i, b in enumerate(data):
        result[i] = b ^ key[i % len(key)]
    return bytes(result)

# Шифрування текстового повідомлення
def encrypt_text(message: str, key: bytes) -> str:
    raw = message.encode("utf-8")
    encrypted = xor_bytes(raw, key)
    return base64.urlsafe_b64encode(encrypted).decode("ascii")

# Розшифрування текстового повідомлення
def decrypt_text(token: str, key: bytes) -> str:
    encrypted = base64.urlsafe_b64decode(token.encode("ascii"))
    decrypted = xor_bytes(encrypted, key)
    return decrypted.decode("utf-8", errors="replace")

# Шифрування файлу (вкладення)
def encrypt_file(path: str, key: bytes) -> str:
    p = Path(path)
    data = p.read_bytes()
    encrypted = xor_bytes(data, key)
    out = p.with_suffix(p.suffix + ".enc")
    out.write_bytes(encrypted)
    return str(out)

# Розшифрування файлу (вкладення)
def decrypt_file(path: str, key: bytes) -> str:
    p = Path(path)
    encrypted = p.read_bytes()
    decrypted = xor_bytes(encrypted, key)
    out = p.with_suffix("") if p.suffix == ".enc" else p.with_name(p.name + ".dec")
    out.write_bytes(decrypted)
    return str(out)

def main():
    # Ввід даних, з яких формується ключ
    email = input("Електронна адреса: ").strip()
    personal = input("Персональні дані для ключа (Ім'яПрізвищеДДММРРРР): ").strip()

    # Генерація спільного секретного ключа
    key = derive_key(email + personal)

    while True:
        print("\n1 - зашифрувати текст")
        print("2 - розшифрувати текст")
        print("3 - зашифрувати файл")
        print("4 - розшифрувати файл")
        print("5 - вихід")

        cmd = input("> ").strip()

        if cmd == "1":
            message = input("Повідомлення: ")
            cipher = encrypt_text(message, key)
            print("Зашифрований текст:")
            print(cipher)

        elif cmd == "2":
            cipher = input("Зашифрований текст: ").strip()
            message = decrypt_text(cipher, key)
            print("Розшифрований текст:")
            print(message)

        elif cmd == "3":
            path = input("Шлях до файлу: ").strip()
            result = encrypt_file(path, key)
            print("Файл зашифровано:", result)

        elif cmd == "4":
            path = input("Шлях до .enc файлу: ").strip()
            result = decrypt_file(path, key)
            print("Файл розшифровано:", result)

        elif cmd == "5":
            break

        else:
            print("Невірна команда")

if __name__ == "__main__":
    main()

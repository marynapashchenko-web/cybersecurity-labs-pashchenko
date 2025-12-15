import hashlib
from pathlib import Path

# Персональні дані
NAME = "Maryna Pashchenko"
BIRTH_DATE = "03.03.2005"
SECRET_WORD = "secret_word"

# Параметри простої математики
MOD = 1_000_007
K = 7

# Хешування тексту (SHA-256)
def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

# Хешування вмісту файлу
def sha256_file_hex(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest()

# Генерація приватного та публічного ключів
def make_keys():
    source = NAME + BIRTH_DATE + SECRET_WORD
    private_hex = sha256_hex(source)
    private_int = int(private_hex, 16) % MOD
    public_int = (private_int * K) % MOD
    return private_int, public_int

# Збереження ключів у файли
def save_keys(private_int: int, public_int: int):
    Path("private.key").write_text(str(private_int), encoding="utf-8")
    Path("public.key").write_text(str(public_int), encoding="utf-8")

# Створення цифрового підпису файлу
def sign_file(file_path: str, private_int: int):
    file_hash_hex = sha256_file_hex(Path(file_path))
    file_hash_int = int(file_hash_hex, 16)
    signature_int = file_hash_int ^ private_int
    Path(file_path + ".sig").write_text(str(signature_int), encoding="utf-8")

# Перевірка цифрового підпису
def verify_file(file_path: str, public_int: int):
    file_path = Path(file_path)

    # якщо користувач ввів .sig, відновлюємо ім'я файлу
    if file_path.suffix == ".sig":
        sig_path = file_path
        file_path = file_path.with_suffix("")
    else:
        sig_path = Path(str(file_path) + ".sig")

    signature_int = int(sig_path.read_text(encoding="utf-8"))

    private_restored = (public_int * pow(K, -1, MOD)) % MOD
    recovered_hash = signature_int ^ private_restored

    current_hash_hex = sha256_file_hex(file_path)
    current_hash_int = int(current_hash_hex, 16)

    if recovered_hash == current_hash_int:
        return "Підпис ДІЙСНИЙ"
    return "Підпис ПІДРОБЛЕНИЙ"


def main():
    # Генерація та збереження ключів
    private_key, public_key = make_keys()
    save_keys(private_key, public_key)

    print("1 - підписати файл")
    print("2 - перевірити підпис")
    print("3 - вихід")

    while True:
        cmd = input("> ").strip()

        if cmd == "1":
            path = input("Введіть ім'я файлу: ").strip()
            sign_file(path, private_key)
            print("Підпис створено")
        elif cmd == "2":
            path = input("Введіть ім'я файлу: ").strip()
            print(verify_file(path, public_key))
        elif cmd == "3":
            break
        else:
            print("Невірна команда")

if __name__ == "__main__":
    main()
